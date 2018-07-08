# coding: utf-8

import logging
import numpy as np
from slackbot.slackclient import SlackClient
from lycee.bot import BotModel


# 重みつき確率による選択
def choice_weight(weight, label):
    wa = np.array(weight) / sum(weight)
    return np.random.choice(label, p=wa)


class Patchouli(BotModel.BotModel):
    REST_MESSAGE = [
        (3, "退屈ね・・・"),
        (3, "紅茶がない・・・昨夜を呼ばないと"),
        (3, "次はこの本を読もうかしら"),
        (1, "また魔理沙に盗られた（´・ω・｀）"),
    ]

    # パチュリーの機嫌度合い（この数値が高いといい返事をしてくれる）

    # 通常の返事
    REPLY_MESSAGE = [
        "なに？",
        "何か御用かしら？",
        "呼んだ？",
    ]

    # 機嫌が悪いときの返事
    GRUMPY_MESSAGE = [
        "うるさいわよ？",
        "本を読んでるの，邪魔しないで",
        "（・・・）"
    ]

    def __init__(self, api_token: str):
        super().__init__('patchouli')
        self.slackClient = SlackClient(
            token=api_token,
            connect=False
        )
        self.channel_list = {}

    def update_channel_list(self):
        response = self.slackClient.webapi.channels.list(True, True)
        if response.successful:
            self.channel_list.clear()
            for ch in filter(lambda c: c['is_member'], response.body['channels']):
                self.channel_list[ch['name']] = ch['id']
            logging.info(self.channel_list)

    def check_pins(self, channel):
        if channel[0] == '#':
            channel = channel[1:]
        elif channel in self.channel_list:
            channel = self.channel_list[channel]
        else:
            logging.info("invalid channel: {}".format(channel))
            return

        response = self.slackClient.webapi.pins.list(channel)
        if response.successful:
            for msg in filter(lambda m: m['type'] == 'message', response.body['items']):
                logging.info(msg)
        else:
            logging.error(response)



