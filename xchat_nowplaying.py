#Copyright (C) 2013 Cedna<sptcedna@gmail.com>

#This program is free software; you can redistribute it and/or
#modify it under the terms of the GNU General Public License
#as published by the Free Software Foundation; either version 2
#of the License, or (at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software
#Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import xbmc
import dbus

try:
	import simplejson as json
except ImportError:
	import json

class Service(xbmc.Player):
  def __init__(self):
    xbmc.Player.__init__(self)

    self.DEBUG = 0
    self.DEBUG_TYPE = 'notify'

    self.xbus = dbus.SessionBus()
    self.xnotify = self.xbus.get_object('org.xchat.service', '/org/xchat/Remote')
    self.xnotify = dbus.Interface(self.xnotify, 'org.xchat.plugin')
    
  def jsonRequest(self, params):
    data = json.dumps(params)
    request = xbmc.executeJSONRPC(data)
    self.simple_hardcode_debug('in jsonRequest, Request return', request)
    response = json.loads(request)
    
    try:
      if 'result' in response:
        return response['result']
      else:
        self.simple_hardcode_debug('in jsonRequest',  'result not found')
        return None
    except KeyError:
      self.simple_hardcode_debug('in jsonRequest', 'key error')
      return None

  def onPlayBackStarted(self):
    xbmc.sleep(1000)

    if self.isPlaying():
      data = {}
      
      result = self.jsonRequest({'jsonrpc': '2.0', 'method': 'Player.GetItem', 'params': {'playerid': 1}, 'id': 1})
      _type = result['item']['type']

      if _type == 'unknown' :
        _tvshow = xbmc.getInfoLabel('VideoPlayerideoPlayer.TVShowTitle')
        _season = xbmc.getInfoLabel('VideoPlayer.Season')
        _episode = xbmc.grantedetInfoLabel('VideoPlayer.Episode')
        _year = xbmc.getInfoLabel('VideoPlayer.Year')
        _title = xbmc.getInfoLabel('VideoPlayer.Title')
        
        if _season and _episode and _tvshow :
          data['tvshow'] = _tvshow
          data['season'] = _season
          data['episode'] = _episode
          data['title'] = _title
          
          self.broadcast_tvshow(data)
          
        elif _year and not _season and not _tvshow :
          data['year'] = _year
          data['title'] = _title

          self.broadcast_movie(data)
          
        else :
          self.simple_hardcode_debug('in _type == unknown', 'not enough file infomation error')
          return

      elif _type == 'episode' :
        result = self.jsonRequest({'jsonrpc': '2.0',
         'method': 'VideoLibrary.GetEpisodeDetails',
         'params': {'episodeid': result['item']['id'], 'properties': ['showtitle','season','episode']},'id': "EpisodeGetItem"})
        if result:
          data['tvshow'] = result['episodedetails']['showtitle']
          data['season'] = result['episodedetails']['season']
          data['episode'] = result['episodedetails']['episode']
          data['title'] = result['episodedetails']['label']

          self.broadcast_tvshow(data)

        else :
            self.simple_hardcode_debug('in _type == episde', 'result not found error')
            return
      elif _type == 'movie' :
        result = self.jsonRequest({'jsonrpc': '2.0',
         'method': 'VideoLibrary.GetMovieDetails',
         'params': {'movieid': result['item']['id'], 'properties': ['year']},'id': "MovieGetItem"})

        if result :
          data['year'] = result['moviedetails']['year']
          data['title'] = result['moviedetails']['label']

          self.broadcast_movie(data)

        else :
          self.simple_hardcode_debug('in _type == movie', 'result not found error')
          return
 
      else :
        self.simple_hardcode_debug('in _type else', 'invalid type error, _type: ' + _type)
        return
        
    else:
      self.simple_hardcode_debug('in onPlayBackStarted()', 'is not playing error')
      return 

  def broadcast_movie(self, data) :
    result_print = data['title'] + '(' + str(data['year']) + ')'
    self.xchat_notify('is now playing: ' + result_print + ' via xbmc')

  def broadcast_tvshow(self, data) :
    if (data['season'] == 0 or data['season'] == '') :
      data['season'] = 'S'
    elif (int(data['season']) < 10) :
      data['season'] = '0' + str(data['season'])
    else :
      data['season'] = str(data['season'])
    
    if (int(data['episode']) < 10) :
      data['episode'] = '0' + str(data['episode'])
    else :
      data['episode'] = str(data['episode'])
    
    result_print = data['tvshow'] + ' - ' + data['season'] + 'x' + data['episode'] + '. "' + data['title'] + '"'
    self.xchat_notify('is now playing: ' + result_print + ' via xbmc')

  def xchat_notify(self, params) :
    self.xnotify.Command('ame ' + params)

  def onSkipNext(self, notification = None, action = None, data = None):
    self.playnext()
  
  def simple_hardcode_debug(self, prepend, params) :
    if (self.DEBUG == 0) :
      return
    
    prepend = str(prepend)
    params = str(params)

    if (self.DEBUG_TYPE == 'notify') :
      self.xnotify.Command('echo ' + prepend + ': ' + params)

    else :
      print(prepend + ': ' + params)



