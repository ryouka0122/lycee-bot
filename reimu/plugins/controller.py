# coding: utf-8

from reimu.bots import Reimu
from slackbot.bot import respond_to, default_reply, settings
from lycee.bot.model import BotModel

# BOT本体
reimu = BotModel.make(Reimu, settings.API_TOKEN)


# 定期実行：天気情報
def task_weather():
    global reimu
    reimu.get_weather_info(
        zipcode='1790085',
        callback=lambda text: reimu.send_message(channel='weather', message=text)
    )


# 初期化
def setup():
    global reimu
    reimu.update_channel_list()
    reimu.add_task('task_weather', '0 7-20 * * *', task_weather)


# 初期化実行
setup()


@respond_to(r'^weather( .+)?$')
def cmd_weather(message, zipcode: str):
    global reimu

    # 前後の不要な空白削除
    zipcode = zipcode.strip()

    reimu.weather(message, zipcode)


@respond_to(r'^zip ([0-9]{7})$')
def cmd_zip(message, zipcode):
    global reimu
    reimu.zip(message, zipcode)


@respond_to(r'^task$')
def command_task(message):
    global reimu
    reimu.show_task_list(message)


@default_reply()
def cmd_default(message):
    text = message.body['text']
    message.reply(text)
