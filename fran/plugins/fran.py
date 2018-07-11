# coding: utf-8

from slackbot.bot import default_reply, respond_to, settings
from fran.bots import Fran

fran = Fran.make(settings.API_TOKEN)

fran.update_channel_list()


@respond_to(r'pin( .+)?$')
def cmd_pin(message, channel: str):
    if channel:
        channel = channel.strip()
    fran.cmd_pin(message, channel)


@default_reply()
def default_func(message):
    text = message.body['text']
    message.reply(text)