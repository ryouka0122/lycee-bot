# coding: utf-8

import random
import time
from slackbot.bot import listen_to, respond_to, default_reply, settings

from lycee.bot.model import BotModelBuilder
from patchouli.bots import Patchouli


def routine():
    global patchouli

    # 発言タイミングを揺らがせる（1分～10分）
    delay_min = random.randrange(1, 10)
    delay_sec = random.randrange(0, 60)
    time.sleep(delay_min * 60 + delay_sec)

    patchouli.routine_chat('test_chat')


# BOT本体
patchouli = BotModelBuilder(Patchouli, settings.API_TOKEN)\
                .task('routineTask', '0 8-20 * * *', routine)\
                .make()


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
