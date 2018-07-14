# coding: utf-8

from remilia.bots import Remilia
from slackbot.bot import respond_to, default_reply, settings
from lycee.bot.model import BotModelBuilder


# 定期実行：天気情報
def task_weather():
    global remilia
    remilia.get_weather_info(
        zipcode='1790085',
        callback=lambda text: remilia.send_message(channel='weather', message=text)
    )


# BOT本体
remilia = BotModelBuilder(Remilia, settings.API_TOKEN)\
    .task('task_weather', '0 7-20 * * *', task_weather)\
    .make()


@respond_to(r'^weather( .+)?$')
def cmd_weather(message, zipcode: str):
    global remilia
    if zipcode:
        remilia.weather(message, zipcode.strip())
    else:
        message.reply('郵便番号が抜けてるよ')


@respond_to(r'^zip ([0-9]{7})$')
def cmd_zip(message, zipcode):
    global remilia
    remilia.zip(message, zipcode)


@respond_to(r'^task$')
def command_task(message):
    global remilia
    remilia.show_task_list(message)


@default_reply()
def cmd_default(message):
    text = message.body['text']
    message.reply(text)
