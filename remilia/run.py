# coding: utf-8

from slackbot.bot import Bot
import os
import sys


# カレントディレクトリをシステムパスに追加
sys.path.append(os.getcwd())


def main():
    bot = Bot()
    bot.run()


if __name__ == "__main__":
    print('start slackbot')
    main()