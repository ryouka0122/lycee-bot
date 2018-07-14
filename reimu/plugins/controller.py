# coding: utf-8

from slackbot.bot import default_reply


@default_reply()
def cmd_default(message):
    text = message.body['text']
    message.reply(text)
