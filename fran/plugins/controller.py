# coding: utf-8

from slackbot.bot import default_reply, respond_to, settings
from lycee.bot.model import BotModel
from fran.bots import Fran


fran = BotModel.make(Fran, settings.API_TOKEN)


@respond_to(r'pin( .+)?$')
def cmd_pin(message, channel: str):
    if channel:
        channel = channel.strip()
    fran.cmd_pin(message, channel)


@respond_to(r'^task$')
def command_task(message):
    global fran
    fran.show_task_list(message)


@default_reply()
def default_func(message):
    text = message.body['text']
    message.reply(text)
