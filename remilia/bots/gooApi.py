# coding: utf-8

import requests
import random as rand
from datetime import datetime


# --------------------------------------------
# GooラボAPI呼び出しクラス
class GooApi(object):

    @staticmethod
    def create_id():
        return 'lycee.slackbot-{}-{:04}'.format(
            datetime.now().strftime('%Y%m%d_%H%M%S.%f'),
            rand.randint(0, 9999)
        )

    def __init__(self, url, api_key):
        self._url = url
        self._api_key = api_key

    def execute_api(self, sentence):
        result = requests.post(self._url, {
            'request_id': self.create_id(),
            'app_id': self._api_key,
            'sentence': sentence
        })
        print(result.json())
        return result


class GooMorphApi(GooApi):
    # 形態素解析API
    API_URL_MORPH = 'https://labs.goo.ne.jp/api/morph'

    def __init__(self, api_key):
        super(GooMorphApi, self).__init__(self.API_URL_MORPH, api_key)
        self._result = []

    def call(self, sentence):
        self._result = self.execute_api(sentence)

    def results(self):
        return self._result


class GooEntityApi(GooApi):
    # 固有表現抽出
    API_URL_ENTITY = 'https://labs.goo.ne.jp/api/entity'

    def __init__(self, api_key):
        super(GooEntityApi, self).__init__(self.API_URL_ENTITY, api_key)
        self._result = []

    def call(self, sentence):
        self._result = self.execute_api(sentence)

    def results(self):
        return self._result


class GooChronoApi(GooApi):
    # 時刻情報解析API
    API_URL_CHRONO = 'https://labs.goo.ne.jp/api/chrono'

    def __init__(self, api_key):
        super(GooChronoApi, self).__init__(self.API_URL_CHRONO, api_key)
        self._result = []

    def call(self, sentence):
        self._result = self.execute_api(sentence)

    def results(self):
        return self._result

