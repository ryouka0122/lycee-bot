# coding: utf-8

import math
from threading import Timer
import logging

from crontab import CronTab


class Task:
    """
        コンストラクタ
        :arg
            name タスク名（管理用情報）
            crontab CronTabに指定するcronフォーマット
            loop 繰り返し回数
            event 定期実行したい呼び出し可能オブジェクト
            args eventに渡したいリスト型動的引数
            kwargs eventに渡したい辞書型動的引数
    """
    def __init__(self, name: str, crontab: str, loop: int, event: callable, *args, **kwargs):
        self.name = name
        self.crontab = CronTab(crontab)

        self.taskEvent = event
        self.taskLoop = loop
        self.timer = None

        self.args = args
        self.kwargs = kwargs
        self.stop_flag = False

    """
        タスクの起動
        :return
            起動に成功したらTrueを返す
            起動中だった場合，Falseを返す
    """
    def start(self) -> bool:
        if self.stop_flag:
            return False
        self.stop_flag = False
        self.run()
        return True

    """
        タスクの停止
    """
    def stop(self):
        self.stop_flag = True
        if self.timer:
            self.timer.cancel()
            self.timer = None

    """
        生存確認
        :return イベントがある時，Trueを返す
    """
    def is_alive(self) -> bool:
        return self.timer is not None

    """
        継続可能確認
        :return 繰り返し回数がまだあるとき，Trueを返す
    """
    def is_continue(self) -> bool:
        if self.stop_flag:
            return False
        self.taskLoop -= 1
        return self.taskLoop > 0

    """
        タイマーの更新
        :return 繰り返し回数分実行された場合，Falseを返す
    """
    def update(self) -> bool:
        if not self.is_continue():
            logging.debug('[{}] Finish Task'.format(self.name))
            return False

        # インターバルの計算（端数切り上げ）
        interval = math.ceil(self.crontab.next(default_utc=False))
        # タイマーの設定
        self.timer = Timer(interval, self.run)
        self.timer.start()
        return True

    """
    タスク実行
    """
    def run(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
            if not self.stop_flag:
                logging.debug('[{}] call event'.format(self.name))
                self.taskEvent(*self.args, **self.kwargs)
        self.update()


class RepeatedTask(Task):
    def __init__(self, name, crontab, event):
        super().__init__(
            name=name,
            crontab=crontab,
            loop=-1,
            event=event)

    """
        継続判定メソッド
        :return
            繰り返し専用タスクなので常にTrue
    """
    def is_continue(self):
        return True


class TaskManager:
    def __init__(self, task_size=100, is_override=True):
        self.task_list = dict()

        self.task_size = task_size
        self.is_override = is_override

    """
        タスクの取得
        :arg
            name 追加時に指定したタスク名
        :return
            タスクオブジェクト
            タスク名が存在しない場合Noneとなる
    """
    def get(self, name: str) -> Task:
        return self.task_list[name] if name in self.task_list else None

    """
        タスクの追加
        :arg
            name: タスク名
                  同一タスク名があった場合，コンストラクタで指定した上書きフラグに応じて上書きを行う
            crontab: CronTabに指定するcronフォーマット
            func: タスクに指定する呼び出し可能オブジェクト
        :return 
            タスクの生成に成功した場合True
            同一タスク名があり，上書きフラグがFalseだった場合，Falseが返る
    """
    def add(self, name: str, crontab: str, func: callable):
        if name in self.task_list:
            if not self.is_override:
                return False
            self.stop(name)

        self.task_list[name] = RepeatedTask(
            name=name,
            crontab=crontab,
            event=func
        )
        return True

    """
        タスクの起動
        :arg
            name 起動させたいタスク名
        :return
            起動に成功するとTrueを返す
            タスクが存在しない場合や起動に失敗するとFalseが返る
    """
    def start(self, name: str) -> bool:
        task = self.get(name)
        if task:
            return task.start()
        return False

    """
        タスクの停止
        :arg
            name 停止させたいタスク名
    """
    def stop(self, name: str):
        task = self.get(name)
        if task:
            task.stop()

    """
        すべてのタスクを停止
    """
    def stop_all(self):
        for name in self.task_list:
            self.task_list[name].stop()

    """
        タスクの除去
        :arg
            name: 除去したいタスク名
    """
    def remove(self, name: str):
        self.stop(name)
        del self.task_list[name]

    """
        すべてのタスクを除去
    """
    def remove_all(self):
        for name in self.task_list:
            self.task_list[name].stop()
        self.task_list.clear()
