# coding: utf-8

import requests
import json

from enum import Enum


# --------------------------------------------------------------------
# REST API用 基底Enum
#
class UrlMethod(Enum):
    """
        URLの生成
        :arg
            end_pont 起点となるURL
        :return
            メソッドを付与した状態のURL
    """
    def make_url(self, end_point: str):
        if end_point[-1:] == '/':
            end_point += '/'
        return end_point + self.value


# --------------------------------------------------------------------
# Slack API用 メソッドEnum
#
class SlackMethod(UrlMethod):
    # チャンネル情報：チャンネル一覧取得
    CHANNELS_LIST = 'channels.list'

    # チャット情報：メッセージの送信
    CHAT_POST_MESSAGE = 'chat.postMessage'

    # ピン止め情報：ピン止め一覧取得
    PINS_LIST = 'pins.list'

    # リアクション情報：リアクションの追加
    REACTIONS_ADD = 'reactions.add'

    # ユーザ情報：ユーザ一覧取得
    USERS_LIST = 'users.ist'


# --------------------------------------------------------------------
# Slack API クラス
#
class SlackApi:
    def __init__(self, api_token: str, end_point: str):
        self.api_token = api_token
        self.end_point = end_point

    """
        APIの呼び出し
        :arg
            method SlackMethodで定義したslack API
            headers ヘッダ情報
            payload リクエスト情報
        :return
            APIのレスポンス情報
    """
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

    """
        チャンネル名からチャンネルIDを取得するメソッド
        :arg
            channel_name チャンネル名
        :return
            チャンネルID
            APIが失敗したり，引数のチャンネル名が存在しない場合，空文字となる
    """
    def get_channel_id(self, channel_name: str) -> str:
        result = self.__call_api(
            method=SlackMethod.CHANNELS_LIST,
            headers={},
            payload={}
        )

        if not result['ok']:
            return ''

        for channelInfo in filter(lambda c: c['is_channel'], result['channels']):
            if channelInfo['name'] == channel_name:
                return channelInfo['id']
        return ''

    """
        指定したチャンネルにあるピン止め情報を取得するメソッド
        :arg
            channel_id: チャンネルID
        :return
            APIのレスポンス情報
    """
    def get_pin_list(self, channel_id: str) -> dict:
        return self.__call_api(
            method=SlackMethod.PINS_LIST,
            headers={},
            payload={
                'channel': channel_id
            }
        )

    """
        メッセージの送信
        発言者は，SLACK_API_TOKENに紐づいたユーザになる
        :arg
            channel_id: チャンネルID
            message: 送信したいメッセージ
        :return
            APIのレスポンス情報
    """
    def send_message(self, channel_id: str, message: str) -> dict:
        return self.__call_api(
            SlackMethod.CHAT_POST_MESSAGE,
            headers={},
            payload={
                'as_user': True,
                'channel': channel_id,
                'text': message
            }
        )
