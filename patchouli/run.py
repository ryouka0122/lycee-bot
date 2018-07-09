# coding: utf-8

import logging
import os
import sys

from slackbot.bot import Bot

# カレントディレクトリをシステムパスに追加
sys.path.append(os.getcwd())

from patchouli.plugins import patchouli

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)5s\t%(message)s',
    datefmt='%Y/%m/%D %H:%M:%S'
)


def main():
    # BOTの生成
    bot = Bot()

    patchouli.setup()

    try:
        # BOT実行
        bot.run()
    except KeyboardInterrupt:
        logging.info('catch KeyboardInterrupt')


if __name__ == "__main__":
    logging.info('start slackbot')
    main()
