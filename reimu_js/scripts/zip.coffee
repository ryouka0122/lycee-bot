# Description:
#   郵便番号から緯度経度を求めるサンプル
#   変換には，http://geoapi.heartrails.com/api.html のAPIを使用
#
# Commands:
#   zip zipcode - GoogleMapのURLを返します（zipcodeはハイフンなし）
#

request = require("request")

calcUtil = require './utils/calcUtil'
urlUtil = require './utils/urlUtil'

COORDINATES_PRECIS = 4

module.exports = (robot) ->

  robot.respond /zip ([0-9]{7})/i, (res) ->
    zipcode=res.match[1]
    console.log "zipcode=" + zipcode

    options =
      url: urlUtil.getGeoApiUrl(zipcode)
      json: false

    request.get options, (err, response, body) ->
      if err
        console.log err
        res.send "geoapi.heartrails.comとの通信に失敗しました"
        return

      json = JSON.parse unescape(body)
      lat = 0.0
      lng = 0.0
      c = 0
      for loc in json["response"]["location"]
        console.log(loc["x"] + " / " + loc["y"])
        lng += parseFloat(loc["x"])
        lat += parseFloat(loc["y"])
        c++
      lng/=c if c>0
      lat/=c if c>0
      lng = calcUtil.roundN(lng, COORDINATES_PRECIS)
      lat = calcUtil.roundN(lat, COORDINATES_PRECIS)
      res.send urlUtil.getGoogleMapUrl(lat, lng)
