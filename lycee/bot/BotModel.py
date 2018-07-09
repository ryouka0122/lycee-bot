# coding: utf-8

from lycee.bot.task import TaskManager


class BotModel:

    """
        コンストラクタ
        :arg
            name: BOT名（識別用）
    """
    def __init__(self, name: str):
        self.name = name
        self.taskManager = TaskManager(task_size=100, is_override=True)

    """
        定期実行タスクの追加
        :arg
            name: タスク名（管理用）
            crontab: CronTabに指定するcronフォーマット
            func: 定期実行したい呼び出し可能オブジェクト
    """
    def add_task(self, name: str, crontab: str, func: callable):
        if self.taskManager.add(name, crontab, func):
            self.taskManager.start(name)

    """
        定期実行タスクの削除
        :arg
            name: タスク名
    """
    def remove_task(self, name):
        self.taskManager.remove(name)

    """
        メッセージ送信
        :arg
            channel 発言したいチャンネル
                    先頭に#をつけるとチャンネル名と識別され，チャンネルIDに自動変換される
            message 送信したいメッセージ
        :return
            APIのレスポンス情報
    """
    def send_message(self, channel: str, message: str) -> dict:
        pass
