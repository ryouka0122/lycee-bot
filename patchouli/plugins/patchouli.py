# coding: utf-8

from slackbot.bot import listen_to, respond_to, default_reply, settings

from patchouli.bots import Patchouli
from lycee.bot.task import TaskManager

# BOT本体
patchouli = Patchouli(settings.API_TOKEN)

# タスク管理
taskManager = TaskManager()


def routine():
    patchouli.check_pins('test_chat')


def setup():
    patchouli.add_task('routineTask', '*/5 * * * *', routine)
    patchouli.update_channel_list()




@respond_to('メンション')
def say(message):
    message.reply('私にメンションと言ってどうするのだ')  # メンション


@respond_to(r'^pin (.+)$')
def pins_list(message, channel):
    global patchouli
    patchouli.check_pins(channel)


@listen_to('リッスン')
def listen_func(message):
    message.send('誰かがリッスンと投稿したようだ')      # ただの投稿
    message.reply('君だね？')                           # メンション


@default_reply()
def default_func(message):
    text = message.body['text']

    message.reply(text)
