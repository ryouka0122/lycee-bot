# coding: utf-8

import logging
import requests

from lycee.bot.BotModel import BotModel
from slackbot.bot import SlackClient

# 座標算出の精度
COORDINATES_PRICIS = 4

DARK_SKY_API_TOKEN="56240d40635d6b21c306a906f7ff10d6"
DARK_SKY_URL = "https://api.darksky.net/forecast/{apiKey}/{lat},{lng}?lang=en&units=si"
GOOGLE_MAP_URL = "https://www.google.com/maps?q={lat},{lng}"
GEO_API_URL = "http://geoapi.heartrails.com/api/json?method=searchByPostal&postal={zipcode}"


def convert_zip_to_coord(zipcode: str) -> dict:
    geo_api_url = GEO_API_URL.format(zipcode=zipcode)

    response = requests.get(url=geo_api_url)
    if not response.ok:
        return {}

    json = response.json()
    if 'error' in json:
        return {}

    lat = 0.0
    lng = 0.0
    c = 0

    for loc in json['response']['location']:
        lng += float(loc['x'])
        lat += float(loc['y'])
        c += 1

    if c > 0:
        lng /= c
        lat /= c

    return {
        'lng': round(lng, COORDINATES_PRICIS),
        'lat': round(lat, COORDINATES_PRICIS)
    }


class Reimu(BotModel):
    ERRMSG_HEARTRAILS = "geoapi.heartrails.comとの通信に失敗しました"

    # BOTリスト（Key=API-KEY / Value=BOT）
    botList = {}

    @staticmethod
    def make(api_token: str):
        if api_token not in Reimu.botList:
            Reimu.botList[api_token] = Reimu(api_token)
        return Reimu.botList[api_token]

    def __init__(self, api_token: str):
        super().__init__('reimu')

        self.slackClient = SlackClient(
            token=api_token,
            connect=True
        )
        self.channel_list = {}

    def update_channel_list(self):
        response = self.slackClient.webapi.channels.list(True, True)
        if response.successful:
            self.channel_list.clear()
            for ch in filter(lambda c: c['is_member'], response.body['channels']):
                self.channel_list[ch['name']] = ch['id']
            logging.info(self.channel_list)

    def get_weather_info(self, zipcode, callback):
        coord = convert_zip_to_coord(zipcode)
        if len(coord) == 0:
            callback(Reimu.ERRMSG_HEARTRAILS)
            return
        dark_sky_url = DARK_SKY_URL.format(
            apiKey=DARK_SKY_API_TOKEN,
            **coord
        )
        response = requests.get(url=dark_sky_url)
        if not response.ok:
            callback("天気情報が取れない！？　え？Σ(ﾟДﾟ)")
            return
        json = response.json()

        weather = json["daily"]["data"][0]["summary"]
        # icon = json["hourly"]["data"][0]["icon"]
        desc = json["daily"]["summary"]
        temperature = round(json["currently"]["temperature"], 1)
        tempMax = round(json["daily"]["data"][0]["temperatureMax"], 1)
        tempMin = round(json["daily"]["data"][0]["temperatureMin"], 1)
        humidity = round(json["daily"]["data"][0]["humidity"] * 100, 0)
        timezone = json["timezone"]
        callback("""
お天気情報だよ [{lat}, {lng} / {timezone}]
天気：{weather}
　　　{desc}
気温：{temperature}℃ ({tempMax}℃ / {tempMin}℃)
湿度：{humidity}％
        """.format(
            lat=coord['lat'], lng=coord['lng'], timezone=timezone,
            weather=weather, desc=desc,
            temperature=temperature, tempMax=tempMax, tempMin=tempMin,
            humidity=humidity)
        )

    def weather(self, message, zipcode):
        self.get_weather_info(zipcode, message.reply)

    def zip(self, message, zipcode):
        coord = convert_zip_to_coord(zipcode)
        if len(coord) > 0:
            message.reply(GOOGLE_MAP_URL.format(**coord))
        else:
            message.reply(Reimu.ERRMSG_HEARTRAILS)

    def send_message(self, channel, message):
        self.slackClient.send_message(channel=channel, message=message)
