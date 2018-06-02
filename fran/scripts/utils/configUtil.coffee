fs = require 'fs'

readFile = (path) ->
  return fs.readFileSync path, 'utf-8'

module.exports = ConfigUtil =
  configData : JSON.parse readFile('./properties/config.json')

  getSlackToken: () ->
    return this.configData.slackToken