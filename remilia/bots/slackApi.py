# coding: utf-8
import requests


class SlackApi:

    def call(self, url, arguments):
        print({
            'url': url,
            'arguments': arguments
            }
        )
        response = requests.post(url, arguments)

        print("API RESULT:{}".format(response))
        return response.json()

    def __init__(self, endpoint, api_token):
        self.apiEndpoint = endpoint
        self.apiToken = api_token

    def channelId(self, channel):
        result = self.call(
                self.apiEndpoint + "/channels.list",
                {
                    'token': self.apiToken
                }
                )

        if result['ok']:
            for channelInfo in result['channels']:
                if channelInfo['name'] == channel and channelInfo['is_channel']:
                    return channelInfo['id']
        return ""

    def pins(self, channel):
        return self.call(
            self.apiEndpoint + "/pins.list",
            {
                'token': self.apiToken,
                'channel': channel
            }
            )
