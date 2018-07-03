# coding: utf-8

from lycee.bot.task import TaskManager
from lycee.bot.slackapi import SlackApi


class BotModel:
    SLACK_API_ENDPOINT = 'https://slack.com/api/'

    def __init__(self, name, slack_api_token: str):
        self.name = name
        self.slackApi = SlackApi(slack_api_token, BotModel.SLACK_API_ENDPOINT)
        self.taskManager = TaskManager(task_size=100, is_override=True)

    def add_task(self, name, crontab, func):
        self.taskManager.add(name, crontab, func)

    def remove_task(self, name):
        self.taskManager.remove(name)

    def call_api(self, headers, payload):
        pass

    def send_message(self, channel: str, message: str):
        if channel[0] != '#':
            channel = self.slackApi.get_channel_id(channel)

        return self.slackApi.send_message(channel, message)


