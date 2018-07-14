# coding: utf-8

import requests
from lycee.bot.model import BotModel

# 座標算出の精度
COORDINATES_PRICIS = 4

DARK_SKY_API_TOKEN = "56240d40635d6b21c306a906f7ff10d6"
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


class Remilia(BotModel):
    ERRMSG_HEARTRAILS = "geoapi.heartrails.comとの通信に失敗しました"

    def __init__(self, api_token: str):
        super().__init__('remilia', api_token)

    def get_weather_info(self, zipcode: str, callback: function):
        coord = convert_zip_to_coord(zipcode)
        if len(coord) == 0:
            callback(Remilia.ERRMSG_HEARTRAILS)
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
        temp_max = round(json["daily"]["data"][0]["temperatureMax"], 1)
        temp_min = round(json["daily"]["data"][0]["temperatureMin"], 1)
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
            temperature=temperature, tempMax=temp_max, tempMin=temp_min,
            humidity=humidity)
        )

    def weather(self, message, zipcode: str):
        self.get_weather_info(zipcode, message.reply)

    def zip(self, message, zipcode: str):
        coord = convert_zip_to_coord(zipcode)
        if len(coord) > 0:
            message.reply(GOOGLE_MAP_URL.format(**coord))
        else:
            message.reply(Remilia.ERRMSG_HEARTRAILS)
