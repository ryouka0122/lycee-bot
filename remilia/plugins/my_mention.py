# coding: utf-8

from functools import reduce
import random
from slackbot.bot import respond_to     # @botname: で反応するデコーダ
from slackbot.bot import listen_to      # チャネル内発言で反応するデコーダ
from slackbot.bot import default_reply  # 該当する応答がない場合に反応するデコーダ
from datetime import datetime, timedelta


from remilia.apis.gooApi import GooMorphApi
from remilia.apis.slackApi import *
from lycee.bot.utils.logger import LogHelper, info, debug, LogLevel

# @respond_to('string')     bot宛のメッセージ
#                           stringは正規表現が可能 「r'string'」
# @listen_to('string')      チャンネル内のbot宛以外の投稿
#                           @botname: では反応しないことに注意
#                           他の人へのメンションでは反応する
#                           正規表現可能
# @default_reply()          DEFAULT_REPLY と同じ働き
#                           正規表現を指定すると、他のデコーダにヒットせず、
#                           正規表現にマッチするときに反応
#                           ・・・なのだが、正規表現を指定するとエラーになる？
# message.reply('string')   @発言者名: string でメッセージを送信
# message.send('string')    string を送信
# message.react('icon_emoji')  発言者のメッセージにリアクション(スタンプ)する
#                               文字列中に':'はいらない

# GOOラボAPIアクセスキー
GOO_API_KEY = 'd3cbf392f9af4cb5e9caca9a338b23c1fb12f8382a4d984a9e06a23c6db900a9'

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

# ログレベルの設定
LogHelper.set_level(LogLevel.INFO)

# リアクション
emotion_list = {
    'nice': ['taba', '100', 'confetti_ball']
}


def my_dump(*args, **kwargs):
    print('-- MY DUMP --')
    for arg in args:
        print("[args]: {}".format(arg))

    for key in kwargs:
        print("[kwargs]: {}={}". format(key, kwargs[key]))


@respond_to(r'^check (.+)$')
@listen_to(r'^check (.+)$')
@info(my_dump)
def check(message, text):
    message.reply(text)


@respond_to('ほめて')
@listen_to('ほめて')
@debug(LogHelper.pre_dump)
def listen_nice(message):
    react_stamp = random.sample(emotion_list['nice'], 1)[0]
    print("react_stamp:" + react_stamp)
    message.react(react_stamp)


@respond_to(r'^pin (.+)$')
@debug(LogHelper.pre_dump)
def info_func(message, channel):
    api = SlackApi('https://slack.com/api/', "xoxb-291993555617-376453222198-ILjYjazutVG3Qj9DF0EoEdgN")
    channel_id = api.channelId(channel)

    if channel_id is '':
        message.send('チャンネル情報が取れなかった．．．')
        return

    result = api.pins(channel_id)
    if result['ok'] is False:
        message.send('{}のピン止めメッセージが取れなかった．．．'.format(channel))
        return

    now = datetime.now()
    response = ''
    count = 0
    marked_item_count = 0
    alerted_item_count = 0

    for item in sorted(
            map(
                lambda x: x['message'],
                filter(
                    lambda x: x['type'] == 'message',
                    result['items']
                )
            ),
            key=lambda x: x['ts'],
            reverse=False
    ):
        print(item)
        count += 1

        mark = ''
        created_time = ts2date(float(item['ts']))  # ピン止めされたメッセージが作成された時間
        past_time = getPastTimeStr(now, created_time)  # 経過時間の算出

        if check_old_date(now, created_time, DEFAULT_PINNED_ITEM_OLD_AGO):
            mark = ':partly_sunny: '  # 晴れ曇りマーク
            marked_item_count += 1

        if check_old_date(now, created_time, ALERT_PINNED_ITEM_OLD_AGO):
            mark = ':fire: '  # 炎マーク
            alerted_item_count += 1

        response += '{mark}{created} ({past}前)\n{link}\n'.format(
            mark=mark,
            created=created_time.strftime('%Y/%m/%d(%a) %H:%M:%S'),
            past=past_time,
            link=item['permalink']
            )

    message.send('ピン止め数：{}\n'.format(count) + response)
    if marked_item_count > 0:
        message.send('古いピン止めメッセージ数：{}'.format(marked_item_count))

    if alerted_item_count > 0:
        message.send(random.choice(ALERT_MESSAGE_LIST).format(alerted_item_count))


@info(pre_hook=LogHelper.pre_dump, post_hook=LogHelper.post_dump)
def check_old_date(current, target, delta):
    return (current - target) > delta


@info(pre_hook=LogHelper.pre_dump, post_hook=LogHelper.post_dump)
def ts2date(ts):
    return datetime.fromtimestamp(ts)


@info(pre_hook=LogHelper.pre_dump, post_hook=LogHelper.post_dump)
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


# @listen_to(r'.+')
@debug(LogHelper.pre_dump)
def listen_func(message):
    text = message.body['text']
    api = GooMorphApi(GOO_API_KEY)
    api.call(text)

    result = api.results().json()
    word_list = result['word_list']
    res = ''
    for word in word_list[0]:
        if '空白' == word[1]:
            continue
        res += '[{}]\n'.format(reduce(lambda a, b: a + ', ' + b, word))
    message.send(res)


@default_reply()
@debug(LogHelper.pre_dump)
def default_func(message):
    print("デフォルトメッセージ")
    listen_func(message)
