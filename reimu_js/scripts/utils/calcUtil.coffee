# Description:
#   none
#
# Notes:
#   計算関連のユーティリティ
#
module.exports = CalcUtil =
  kerbin2celsius : (K) ->
    return K - 273.15

  roundN : (num, precis) ->
    rank = Math.pow(10, precis)
    return Math.round(num * rank) / rank
