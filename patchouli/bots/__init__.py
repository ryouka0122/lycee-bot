# coding: utf-8

import logging
import numpy as np
import random

from datetime import datetime, timedelta
from lycee.bot.model import BotModel
from lycee.common import convert_text


# 重みつき確率による選択
def choice_weight(weight, label):
    wa = np.array(weight) / sum(weight)
    return np.random.choice(label, p=wa)


class Patchouli(BotModel):

    # ピン止めメッセージの基準日数
    DEFAULT_PINNED_ITEM_OLD_AGO = timedelta(days=14)

    # 文句を言う基準日数
    ALERT_PINNED_ITEM_OLD_AGO = timedelta(days=18)

    # 文句のセリフリスト
    ALERT_MESSAGE_LIST = [
        '{}個も放置してるの？しっかりしてよね！？',
        '{}個も溜まってるわよ？',
        '散らかってるじゃない・・・早く片付けなさい :anger:',
        '放置してるピン止めメッセージがあるなんて・・・ :sweat_drops:',
    ]

    REST_MESSAGE = [
        (3, "退屈ね・・・"),
        (3, "紅茶がない・・・昨夜を呼ばないと"),
        (3, "次はこの本を読もうかしら"),
        (1, "また魔理沙に盗られた（´・ω・｀）"),
    ]

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
        super().__init__('patchouli', api_token)

        # パチュリーの機嫌度合い（この数値が高いといい返事をしてくれる）
        self.mind_health = 30

    def routine_chat(self, channel):
        (weight, label) = zip(*Patchouli.REST_MESSAGE)
        msg = choice_weight(weight, label)
        logging.info('message: {}'.format(msg))
        self.slackClient.send_message(
            channel=self.channel_list[channel],
            message=msg
        )

    def check_pins(self, message, channel):
        logging.info(self.channel_list)

        if channel[0] == '#':
            channel = channel[1:]
        elif channel in self.channel_list:
            channel = self.channel_list[channel]
        else:
            logging.info("invalid channel: {}".format(channel))
            return

        response = self.slackClient.webapi.pins.list(channel)
        if not response.successful:
            message.send('{}のピン止めメッセージが取れなかった．．．'.format(channel))
            return

        now = datetime.now()
        res_msg = ''
        count = 0
        marked_item_count = 0
        alerted_item_count = 0

        for item in sorted(
                map(
                    lambda x: x['message'],
                    filter(
                        lambda x: x['type'] == 'message',
                        response.body['items']
                    )
                ),
                key=lambda x: x['ts'],
                reverse=False
        ):
            print(item)
            count += 1

            mark = ''
            created_time = datetime.fromtimestamp(float(item['ts']))  # ピン止めされたメッセージが作成された時間
            past_time = convert_text(now - created_time)  # 経過時間の算出

            if Patchouli.check_old_date(now, created_time, Patchouli.DEFAULT_PINNED_ITEM_OLD_AGO):
                mark = ':partly_sunny: '  # 晴れ曇りマーク
                marked_item_count += 1

            if Patchouli.check_old_date(now, created_time, Patchouli.ALERT_PINNED_ITEM_OLD_AGO):
                mark = ':fire: '  # 炎マーク
                alerted_item_count += 1

            res_msg += '{mark}{created} ({past})\n{link}\n'.format(
                mark=mark,
                created=created_time.strftime('%Y/%m/%d(%a) %H:%M:%S'),
                past=past_time,
                link=item['permalink']
            )

        message.send('ピン止め数：{}\n'.format(count) + res_msg)
        if marked_item_count > 0:
            message.send('古いピン止めメッセージ数：{}'.format(marked_item_count))

        if alerted_item_count > 0:
            message.send(random.choice(Patchouli.ALERT_MESSAGE_LIST).format(alerted_item_count))

    @staticmethod
    def check_old_date(current, target, delta):
        return (current - target) > delta
