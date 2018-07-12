# coding: utf-8

import logging

from lycee.bot.task import TaskManager
from slackbot.bot import SlackClient


class BotModel:

    # BOTリスト（Key=API-KEY / Value=BOT）
    botList = {}

    @staticmethod
    def make(cls, api_token: str):
        if api_token not in BotModel.botList:
            BotModel.botList[api_token] = cls(api_token)
        return BotModel.botList[api_token]

    """
        コンストラクタ
        :arg
            name: BOT名（識別用）
            api_token: Slack API Token
    """
    def __init__(self, name: str, api_token: str):
        self.name = name
        self.taskManager = TaskManager(task_size=100, is_override=True)

        self.slackClient = SlackClient(
            token=api_token,
            connect=True
        )
        self.channel_list = {}
        self.update_channel_list()

    """
        BOTが識別できるチャンネルのリストを更新
    """
    def update_channel_list(self):
        response = self.slackClient.webapi.channels.list(True, True)
        if response.successful:
            self.channel_list.clear()
            for ch in filter(lambda c: c['is_member'], response.body['channels']):
                self.channel_list[ch['name']] = ch['id']
            logging.debug(self.channel_list)

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

    """
        タスク一覧表示
    """
    def show_task_list(self, message):
        response = ''
        for taskName, task in self.taskManager.task_list.iteritems():
            response += '{} : {}\n'.format(taskName, task.crontabStr)

        if response != '':
            message.send(response)