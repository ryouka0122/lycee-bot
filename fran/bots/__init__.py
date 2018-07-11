# coding: utf-8

import logging
from lycee.bot.BotModel import BotModel
from slackbot.bot import SlackClient

from datetime import datetime


def ts2date(ts):
    return datetime.fromtimestamp(ts)


def getPastTimeStr(now, old):
    delta = now - old
    spent_time = delta.total_seconds()
    spent_time /= 60  # 秒数はいらないから破棄

    spent_str = ''
    if spent_time % 60 > 0:
        spent_str = '%02d分' % (spent_time % 60)
        spent_time /= 60

    if spent_time % 24 > 0:
        spent_str = ('%02d時間' % (spent_time % 24)) + spent_str
        spent_time /= 24

    if spent_time > 0:
        spent_str = ('%d日' % spent_time) + spent_str

    return spent_str


class Fran(BotModel):

    # BOTリスト（Key=API-KEY / Value=BOT）
    botList = {}

    @staticmethod
    def make(api_token: str):
        if api_token not in Fran.botList:
            Fran.botList[api_token] = Fran(api_token)
        return Fran.botList[api_token]

    def __init__(self, api_token: str):
        super().__init__('fran')

        self.slackClient = SlackClient(
            token=api_token,
            connect=True
        )
        self.channel_list = {}

    def update_channel_list(self):
        response = self.slackClient.webapi.channels.list(True, True)
        if response.successful:
            self.channel_list.clear()
            for ch in filter(lambda c: c['is_member'], response.body['channels']):
                self.channel_list[ch['name']] = ch['id']
            logging.info(self.channel_list)

    def cmd_pin(self, message, channel):
        if channel is None or channel == '':
            message.reply('見たいチャンネルを教えて')
            return

        if channel not in self.channel_list:
            message.reply('そのチャンネル，わたし知らないんだけど :anger:')
            return

        response = self.slackClient.webapi.pins.list(self.channel_list[channel])

        if not response.successful:
            message.reply('ピン止め情報が取れなかった．．．')
            return
        text = ''
        current = datetime.now()
        for item in sorted(
            map(
                lambda i: i['message'],
                filter(
                    lambda i: i['type'] == 'message',
                    response.body['items']),
            ),
            key=lambda x: x['ts'],
            reverse=False
        ):
            created_time = ts2date(float(item['ts']))
            spent_time = getPastTimeStr(current, created_time)
            text += """
{created_time}({spent_time}前)
{permalink}
            """.format(
                created_time=created_time,
                spent_time=spent_time,
                permalink=item['permalink']
            )
        message.reply(text)





