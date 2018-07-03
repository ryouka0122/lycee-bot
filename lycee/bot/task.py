# coding: utf-8

import math
from threading import Timer
import logging

from crontab import CronTab


class Task:
    '''
        コンストラクタ
        :arg name タスク名（管理用情報）
        :arg crontab CronTabに指定するcronフォーマット
        :arg loop 繰り返し回数
        :arg event 定期実行したい呼び出し可能オブジェクト
        :arg args eventに渡したいリスト型動的引数
        :arg kwargs eventに渡したい辞書型動的引数
    '''
    def __init__(self, name, crontab, loop, event, *args, **kwargs):
        self.name = name
        self.crontab = CronTab(crontab)

        self.taskEvent = event
        self.taskLoop = loop
        self.timer = None

        self.args = args
        self.kwargs = kwargs
        self.stop_flag = False

    def stop(self):
        self.stop_flag = True

    '''
        生存確認
        :return イベントがある時，Trueを返す
    '''
    def is_alive(self) -> bool:
        return self.timer is not None

    '''
        継続可能確認
        :return 繰り返し回数がまだあるとき，Trueを返す
    '''
    def is_continue(self) -> bool:
        if self.stop_flag:
            return False
        self.taskLoop -= 1
        return self.taskLoop > 0

    '''
        タイマーの更新
        :return 繰り返し回数分実行された場合，Falseを返す
    '''
    def update(self) -> bool:
        if not self.is_continue():
            logging.info('[{}] Finish Task'.format(self.name))
            return False

        # インターバルの計算（端数切り上げ）
        interval = math.ceil(self.crontab.next(default_utc=False))
        # タイマーの設定
        self.timer = Timer(interval, self.run)
        self.timer.start()
        return True

    '''
    タスク実行
    '''
    def run(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
            if not self.stop_flag:
                logging.info('[{}] call event'.format(self.name))
                self.taskEvent(*self.args, **self.kwargs)
        self.update()


class RepeatedTask(Task):
    def __init__(self, name, crontab, event):
        super().__init__(
            name=name,
            crontab=crontab,
            loop=-1,
            event=event)

    def is_continue(self):
        return True


class TaskManager:
    def __init__(self, task_size=100, is_override=True):
        self.task_list = dict()

        self.task_size = task_size
        self.is_override = is_override

    def get(self, name) -> Task:
        return self.task_list[name] if name in self.task_list else None

    def add(self, name, crontab, func):
        if name in self.task_list:
            if not self.is_override:
                return False
            self.stop(name)

        self.task_list[name] = RepeatedTask(
            name=name,
            crontab=crontab,
            event=func
        )

    def stop(self, name):
        task = self.get(name)
        if task:
            task.stop()

    def remove(self, name):
        self.stop(name)
        del self.task_list[name]


