# Description:
#   Example scripts for you to examine and try out.
#
# Commands:
#   weather - 天気情報を返します
#   weather city - その場所の天気情報を返します
#   weather zipcode - 郵便番号から場所を特定して，その場所の天気情報を返します
#
# Notes:
#   They are commented out by default, because most of them are pretty silly and
#   wouldn't be useful and amusing enough for day to day huboting.
#   Uncomment the ones you want to try and experiment with.
#
#   These are from the scripting documentation: https://github.com/github/hubot/blob/master/docs/scripting.md

CronJob = require('cron').CronJob

request = require 'request'

calcUtil = require './utils/calcUtil'
urlUtil = require './utils/urlUtil'

privateInfo = require './privateInfo'

COORDINATES_PRECIS = 4

DARKSKY_API_KEY = privateInfo.getDarkSkyApiKey()


getWeatherInfo = (zipCode, callback) ->
  bFinished = false

  options =
    url: urlUtil.getGeoApiUrl(zipCode)
    json: false

  request.get options, (err, response, body) ->
    if err
      console.log err
      callback "geoapi.heartrails.comとの通信に失敗しました"
      bFinished = true
      return

    json = JSON.parse unescape(body)
    c = 0
    lat = 0.0
    lng = 0.0
    for loc in json["response"]["location"]
      console.log(loc["x"] + " / " + loc["y"])
      lng += parseFloat(loc["x"])
      lat += parseFloat(loc["y"])
      c++
    lng/=c if c>0
    lat/=c if c>0
    lng = calcUtil.roundN(lng, COORDINATES_PRECIS)
    lat = calcUtil.roundN(lat, COORDINATES_PRECIS)

    options =
      url: urlUtil.getDarkSkyUrl(DARKSKY_API_KEY, lat, lng)
      json: false

    console.log options.url

    request.get options, (err, response, body) ->
      if err
        console.log err
        callback "天気情報が取れない！？　え？Σ(ﾟДﾟ)"
        return

      json = JSON.parse body

      weather = json["daily"]["data"][0]["summary"]
      icon = json["hourly"]["data"][0]["icon"]
      desc = json["daily"]["summary"]
      tempature = calcUtil.roundN(json["currently"]["temperature"],1)
      tempMax = calcUtil.roundN(json["daily"]["data"][0]["temperatureMax"],1)
      tempMin = calcUtil.roundN(json["daily"]["data"][0]["temperatureMin"],1)
      humidity = calcUtil.roundN(json["daily"]["data"][0]["humidity"] * 100, 0)
      timezone = json["timezone"]
      callback """お天気情報だよ [#{lat}, #{lng} / #{timezone}]
                  天気：#{weather}
                  　　　#{desc}
                  気温：#{tempature}℃ (#{tempMax}℃ / #{tempMin}℃)
                  湿度：#{humidity}％
                  """

module.exports = (robot) ->
  defaultCity = "Tokyo"
  defaultZipCode = "1030028"

  wheaterInfoJob = new CronJob(
    cronTime: "0 0 7-20 * * *"
    start: true
    timeZone: "Asia/Tokyo"
    onTick: ->
      getWeatherInfo defaultZipCode, (info) ->
        robot.send {
          room: "#weather"
        }, info
  )

  robot.respond /weather( .+)?/i, (res) ->
    param = ""
    zipcode = defaultZipCode

    if res.match[1]?
      param = res.match[1]?.trim().replace("-", "")
      console.log "param=#{param}"
      if /[0-9]{7}/.test(param)
        zipcode = param

    console.log "zipcode=#{zipcode}"

    getWeatherInfo zipcode, (info) ->
      res.send info
