# Description:
#
# Commands:
#
# Notes:
#

request = require 'request'

configUtil = require './utils/configUtil'
urlUtil = require './utils/urlUtil'


module.exports = (robot) ->

  robot.respond /pin/i, (res) ->
    request.post
      url: urlUtil.getSlackPinsList()
      form:
        token: configUtil.getSlackToken()
        channel: 'CAZRSGBK3'  # billboard
    , (err, response, body) ->
      json = JSON.parse unescape(body)
      if !json.ok
        res.send """
                  ピン止め情報が取れなかった．．．
                  [#{json.error}]
                  """
        return
      message = ""
      curDate = new Date();
      for item in json.items
        if item.type == "message"
          createdDate = new Date()
          createdDate.setTime(item.created * 1000)
          spentTime = Math.floor( (curDate.getTime() - createdDate.getTime()) / (1000 * 60) );

          if Math.floor(spentTime/60) > 0
            sH = Math.floor(spentTime/60) + "時間"
          else
            sH = ""

          if spentTime % 60 > 0
            sM = spentTime % 60 + "分"
          else
            sM = ""
          message = """
                    #{createdDate.toISOString()}(#{sH}#{sM}前)
                    #{item.message.permalink}
                    #{message}
                    """

      message = """
                ピン止め数：#{json.items.length}
                #{message}
                """
      res.send message

#  robot.respond /token/i, (res) ->
#    res.send configUtil.getSlackToken()
