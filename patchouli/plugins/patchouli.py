# coding: utf-8

import logging
from slackbot.bot import listen_to, respond_to, default_reply, settings
from patchouli.bots import Patchouli


# BOT本体
patchouli = Patchouli.make(settings.API_TOKEN)


def routine():
    global patchouli
    patchouli.routine_chat('test_chat')


def setup():
    global patchouli
    patchouli.add_task('routineTask', '0 8-20 * * *', routine)
    patchouli.update_channel_list()


@respond_to('メンション')
def say(message):
    global patchouli
    message.reply('私にメンションと言ってどうするのだ')  # メンション


@respond_to(r'^pin (.+)$')
def pins_list(message, channel):
    global patchouli
    patchouli.check_pins(message, channel)


@respond_to(r'^task$')
def command_task(message):
    global patchouli
    patchouli.show_task_list(message)


@listen_to('リッスン')
def listen_func(message):
    global patchouli
    message.send('誰かがリッスンと投稿したようだ')      # ただの投稿
    message.reply('君だね？')                           # メンション


@default_reply()
def default_func(message):
    global patchouli
    text = message.body['text']
    message.reply(text)
