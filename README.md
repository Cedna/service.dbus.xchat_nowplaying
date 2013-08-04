XChat now playing Add-on for XBMC
=================================
A XBMC Add-on for publishes current playing media data information to XChat.

Turn on DEBUG
--------------
Change self.DEBUG value to 1

```
#xchat_nowplaying.py

class Service(xbmc.Player):
  def __init__(self):
    xbmc.Player.__init__(self)

    self.DEBUG = 1 #DEFAULT is 0
    self.DEBUG_TYPE = 'notify'
```

Contact
--------
* Mail: sptcedna@gmail.com
* Twitter: @sptcedna
* IRC: Cedna(irc.rizon.net)
* IRC(Korean): Cedna(kr.hanirc.org)

LICENSE
--------
GPL V2, see [LICENSE](/LICENSE) for more detail.

Source Code References
-----------------------
* [D-Bus notification service, GPL V2](http://wiki.xbmc.org/index.php?title=Add-on:D-Bus_notification_service)
* [trakt for XBMC, GPL V2](https://github.com/rectifyer/script.trakt)

