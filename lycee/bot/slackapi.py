# coding: utf-8

import requests
import json

from enum import Enum


class UrlMethod(Enum):
    def make_url(self, end_point: str):
        if end_point[-1:] == '/':
            end_point += '/'
        return end_point + self.value


class SlackMethod(UrlMethod):
    CHANNELS_LIST = 'channels.list'
    CHAT_POST_MESSAGE = 'chat.postMessage'
    PINS_LIST = 'pins.list'

    REACTIONS_ADD = 'reactions.add'
    USERS_LIST = 'users.ist'


class SlackApi:
    def __init__(self, api_token: str, end_point: str):
        self.api_token = api_token
        self.end_point = end_point

    def __call_api(self, method: SlackMethod, headers: dict, payload: dict) -> dict:
        # 共通情報の追加
        _headers = headers if isinstance(headers, dict) else dict()
        _headers['Content-type'] = 'application/json; charset=UTF-8'
        _headers['Authorization'] = 'Bearer ' + self.api_token

        # API呼び出し
        response = requests.post(
            url=method.make_url(self.end_point),
            headers=_headers,
            data=json.dumps(payload)
        )
        # 戻り値を辞書型に変換
        return response.json()

    def get_channel_id(self, channel_name: str) -> str:
        result = self.__call_api(SlackMethod.CHANNELS_LIST, {})

        if not result['ok']:
            return ''

        for channelInfo in filter(lambda c: c['is_channel'], result['channels']):
            if channelInfo['name'] == channel_name:
                return channelInfo['id']
        return ''

    def get_pin_list(self, channel_id: str) -> dict:
        return self.__call_api(
            SlackMethod.PINS_LIST,
            {
                'channel': channel_id
            }
        )

    def send_message(self, channel_id: str, message: str):
        return self.__ca_api(
            SlackMethod.CHAT_POST_MESSAGE,
            {
                'as_user': True,
                'channel': channel_id,
                'text': message
            }
        )