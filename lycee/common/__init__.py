# coding: utf-8

from datetime import timedelta


def convert_text(delta: timedelta, suffix: str ='前') -> str:
    spent_time = delta.total_seconds()
    spent_time /= 60  # 秒数はいらないから破棄
    if spent_time == 0:
        return 'たった今'

    spent_str = ''

    if spent_time % 60 > 0:
        spent_str = '%02d分' % (spent_time % 60) + spent_str
        spent_time /= 60

    if spent_time % 24 > 0:
        spent_str = ('%02d時間' % (spent_time % 24)) + spent_str
        spent_time /= 24

    if spent_time > 0:
        spent_str = ('%d日' % spent_time) + spent_str

    spent_str += suffix
    return spent_str
