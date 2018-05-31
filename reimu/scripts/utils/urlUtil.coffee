# Description:
#   none
#
# Notes:
#   URLを生成
#
module.exports = UrlUtil =
  getGoogleMapUrl : (lat, lng) ->
    return "https://www.google.com/maps?q=#{lat},#{lng}"

  getDarkSkyUrl : (apiKey, lat, lng) ->
    return "https://api.darksky.net/forecast/#{apiKey}/#{lat},#{lng}?lang=en&units=si"

  getOpenWeatherMapUrl : (appid, city) ->
    return "http://api.openweathermap.org/data/2.5/weather?appid=#{appid}&q=#{city},jp"

  getGeoApiUrl : (zipCode) ->
    return "http://geoapi.heartrails.com/api/json?method=searchByPostal&postal=#{zipCode}"
