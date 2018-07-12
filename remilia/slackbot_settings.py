# coding: utf-8

import json

private_settings = None


def load_token(key: str) -> str:
    global private_settings
    if private_settings is None:
        f = open('private\rconfig_remilia.json')
        private_settings = json.load(f)
        f.close()

    return private_settings[key] if key in private_settings else ''


# botアカウントのトークンを指定
API_TOKEN = load_token('slackApiToken')

# このbot宛のメッセージで、どの応答にも当てはまらない場合の応答文字列
DEFAULT_REPLY = "何言ってんだこいつ"

# プラグインスクリプトを置いてあるサブディレクトリ名のリスト
PLUGINS = ['plugins']