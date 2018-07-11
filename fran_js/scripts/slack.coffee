# Description:
#
# Commands:
#
# Notes:
#

request = require 'request'
_async = require 'async'

configUtil = require './utils/configUtil'
urlUtil = require './utils/urlUtil'

convertSpentTime = (spentTime) ->
  result = ""
  if Math.floor( spentTime/(60*24) ) > 0
    result += Math.floor( spentTime/(60*24) ) + "日"
    spentTime = spentTime % (60*24)

  if Math.floor(spentTime/60) > 0
    result += Math.floor(spentTime/60) + "時間"
    spentTime = spentTime % 60

  if spentTime > 0
    result += spentTime + "分"

  return result

module.exports = (robot) ->

  robot.respond /pin( .*)/i, (res) ->
    curDate = new Date()
    _async.waterfall([
      (callback) ->
        if res.match?.length == 0
          callback "error", "どのチャンネルのピン止めを見たいの？？"
        else
          callback null, res.match[1].trim()

      , (channelName, callback) ->
        request.post
          url: urlUtil.getSlackChannelsList()
          form:
            token: configUtil.getSlackToken()
          , (err, response, body) =>
            json = JSON.parse unescape(body)
            channelId=""
            if json.ok
              for channel in json.channels
                if channel.name == channelName
                  channelId = channel.id
            console.log "channelName=#{channelName} / channelId=#{channelId}"
            callback null, channelId

      , (channelId, callback) ->
        console.log "channelId=#{channelId}"

        request.post
          url: urlUtil.getSlackPinsList()
          form:
            token: configUtil.getSlackToken()
            channel: channelId
          , (err, response, body) ->
            json = JSON.parse unescape(body)
            if !json.ok
              callback "error", """
                        ピン止め情報が取れなかった．．．
                        [#{json.error}]
                        """
              return

            items = json.items.filter (item) ->
              return item.type == "message"
            callback null, items

      , (items, callback) ->
        message = ""
        for item in items
          createdDate = new Date()
          createdDate.setTime(item.created * 1000)
          spentMinutes = Math.floor( (curDate.getTime() - createdDate.getTime()) / (1000 * 60) );
          spentTime = convertSpentTime(spentMinutes)
          message = """
                    #{createdDate.toISOString()}(#{spentTime}前)
                    #{item.message.permalink}
                    #{message}
                  """
        callback null, """
                  ピン止め数：#{items.length}
                  #{message}
                  """
    ], (err, result) ->
      res.send result
    )
