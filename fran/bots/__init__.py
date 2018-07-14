# coding: utf-8

from datetime import datetime

from lycee.bot.model import BotModel
from lycee.common import convert_text


class Fran(BotModel):

    def __init__(self, api_token: str):
        super().__init__('fran', api_token)

    def cmd_pin(self, message, channel: str):
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
            created_time = datetime.fromtimestamp(float(item['ts']))
            spent_time = convert_text(current - created_time)
            text += """
{created_time}({spent_time})
{permalink}
            """.format(
                created_time=created_time,
                spent_time=spent_time,
                permalink=item['permalink']
            )
        message.reply(text)
