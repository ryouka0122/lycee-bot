# coding: utf-8

from datetime import datetime
from lycee.bot.model import BotModel


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

    def __init__(self, api_token: str):
        super().__init__('fran', api_token)

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





