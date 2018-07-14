# coding: utf-8

from lycee.bot.model import BotModel


class Reimu(BotModel):

    def __init__(self, api_token: str):
        super().__init__('reimu', api_token)
