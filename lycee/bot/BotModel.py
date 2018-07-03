# coding: utf-8

from lycee.bot.task import TaskManager
from lycee.bot.slackapi import SlackMethod, SlackApi


class BotModel:
    SLACK_API_ENDPOINT = 'https://slack.com/api/'

    def __init__(self, name: str, slack_api_token: str):
        self.name = name
        self.slackApi = SlackApi(slack_api_token, BotModel.SLACK_API_ENDPOINT)
        self.taskManager = TaskManager(task_size=100, is_override=True)

    """
        定期実行タスクの追加
        :arg
            name: タスク名（管理用）
            crontab: CronTabに指定するcronフォーマット
            func: 定期実行したい呼び出し可能オブジェクト
    """
    def add_task(self, name: str, crontab: str, func: callable):
        self.taskManager.add(name, crontab, func)

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
        if channel[0] != '#':
            channel = self.slackApi.get_channel_id(channel[1:])
        if channel == '':
            return dict()
        return self.slackApi.send_message(channel, message)
