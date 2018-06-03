# Description:
#   Example scripts for you to examine and try out.
#
# Notes:
#   They are commented out by default, because most of them are pretty silly and
#   wouldn't be useful and amusing enough for day to day huboting.
#   Uncomment the ones you want to try and experiment with.
#
#   These are from the scripting documentation: https://github.com/github/hubot/blob/master/docs/scripting.md

request = require 'request'
xml2js = require 'xml2js'
_async = require 'async'

urlUtil = require './utils/urlUtil'
configUtil = require './utils/configUtil'


module.exports = (robot) ->
  robot.respond /(.*)/i, (res) ->
    msg = res.match[1]

    if !msg || /(ぱちぇ|ぱちゅりー|パチェ|パチュリー)/i.test msg
      res.send "何か御用かしら？"
      return

    _async.waterfall([
      (callback) ->
        options =
          url: urlUtil.getYahooParseApiUrl()
          form:
            appid: configUtil.getYahooAppId()
            sentence: msg
            results: "ma"
          json: false
        callback(null, options)
      , (options, callback) ->
        request.post options, (err, response, body) ->
          if err
            callback "error", err
            return
          console.log "response.statusCode=#{response.statusCode}"
          console.log body
          xml2js.parseString body, (err, result) ->
            if err
              callback "error", result
            else
              callback null, result

      , (result, callback) ->
        if result.Error?
          callback 'error', result.Error.Message
        message = "\n"
        for word in result.ResultSet.ma_result[0].word_list[0].word
          console.log "* * word * *"
          console.log word
          message += "#{word.surface[0]}: #{word.pos[0]}\n"
        callback null, message
      ], (err, result) ->
        if err
          console.log result
        res.reply "#{result}"
      )
