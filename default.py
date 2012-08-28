#!/usr/bin/python
# -*- coding: utf8 -*-
"""
Plugin which shows all artists. This is independent from system settings.
You can use Music->Artists to show only artists with albums or singles
and this plugin to show all artists.
"""

import urllib, urllib2, re, xbmcplugin, xbmcaddon, xbmcgui, xbmc, os
import json

# All artists by xycl

def playSong(artistid, albumid, pos):
    # create a playlist
    playlist = xbmc.PlayList(0)
    # clear the playlist
    playlist.clear()
    counter=0

    json_songs = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": { "sort": { "ignorearticle": true, "method": "track", "order": "ascending" }, "properties": ["file", "thumbnail", "fanart", "track", "rating", "duration", "album", "artist", "genre", "year", "comment"], "albumid": ' + albumid + ', "artistid": ' + artistid + '}, "id": 1}')
    result = json.loads(json_songs)
    if result["result"] != None:
        songs = result["result"]["songs"]

        for content in songs:
            liz = makeListItem(content["label"], content["thumbnail"], content["fanart"], content["track"], content["rating"], content["duration"], content["album"], content["artist"], content["genre"], content["year"], content["comment"])
            playlist.add( content["file"], liz )
            counter=counter+1

        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.Open", "params": { "item": { "playlistid": 0, "position" : '+ pos +' } }, "id": 1 }')

def makeListItem(label, thumbnail, fanart, track, rating, duration, album, artist, genre, year, comment):
    liz=xbmcgui.ListItem( label, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    liz.setInfo( type="music", infoLabels={ "title": label, "tracknumber": track, "rating": str(rating) , "duration": duration, "album":album, "artist":artist, "genre": genre, "year":year, "comment":comment } )
    liz.setProperty( "Fanart_Image", fanart )
    return liz
    
def showSongs(artistid, albumid):

    counter=0

    json_songs = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": { "sort": { "ignorearticle": true, "method": "track", "order": "ascending" }, "properties": ["file", "thumbnail", "fanart", "track", "rating", "duration", "album", "artist", "genre", "year", "comment"], "albumid": ' + albumid + ', "artistid": ' + str(artistid) + '}, "id": 1}')
    result = json.loads(json_songs)
    if result["result"] != None:
        songs = result["result"]["songs"]
        for content in songs:
            listitem = addSong(content["label"], artistid, albumid, str(counter),3, content["thumbnail"], content["fanart"], content["track"], content["rating"], content["duration"], content["album"], content["artist"], content["genre"], content["year"], content["comment"], content["file"])
            counter=counter+1

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TRACKNUM)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_SONG_RATING)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addSong(name, artistid, albumid, pos,mode,iconimage, fanart, track, rating, duration, album, artist, genre, year, comment, file):
    u=sys.argv[0]+"?artistid="+str(artistid)+"&albumid="+str(albumid)+"&pos="+str(pos)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="music", infoLabels={ "title": name, "tracknumber": track, "rating": str(rating), "duration": duration, "album":album, "artist":artist, "genre": genre, "year":year, "comment":comment } )
    liz.setProperty( "Fanart_Image", fanart )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok
        
def showAlbums(artistid):
    json_album = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": {"sort": { "ignorearticle": true, "method": "album", "order": "ascending" }, "properties": ["thumbnail", "fanart", "year", "artist", "genre"], "artistid": ' + artistid + '}, "id": 1}')
    result = json.loads(json_album)
    if result["result"] != None:
        albums = result["result"]["albums"]
        for content in albums:
            addAlbumsDir(content["label"], artistid, content["albumid"], 2, content["thumbnail"], content["fanart"], content["year"], content["artist"], content["genre"])
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_ALBUM_IGNORE_THE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)
    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addAlbumsDir(name, artistid, albumid, mode, iconimage, fanart, date, artist, genre):
    u=sys.argv[0]+"?artistid="+str(artistid)+"&albumid="+str(albumid)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
    ok=True
    if str(date) == "0":
        datum = " "
    else:
        datum = str(date)

    liz=xbmcgui.ListItem(label=artist +" - "+name, label2=datum, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="music", infoLabels={ "album": name , "year":date, "genre": genre,"artist":artist, "title": name, "Label2": artist, "Title": artist} )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setLabel2(datum)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok
        
def showArtists():
    json_artists = xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": {"properties": ["thumbnail", "fanart", "genre", "description", "style"], "albumartistsonly": false, "sort": { "ignorearticle": true, "method": "artist", "order": "ascending" } }, "id": 1}')
    result = json.loads(json_artists)

    if result["result"] != None:
        artists = result["result"]["artists"]
        totalitems = len(artists)
        list = []
        for content in artists:
            list.append(addArtistsDir(content["label"], content["artistid"], 1, content["thumbnail"], content["fanart"], content["description"], content["genre"], content["style"], totalitems))

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

def addArtistsDir(name, artistid, mode, iconimage, fanart, description, genre, style, items):
    u=sys.argv[0]+"?artistid="+str(artistid)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="music", infoLabels={ "artist": name , "artistid": artistid} )
    liz.setProperty( "Fanart_Image", fanart)
    liz.setProperty( "Artist_Description", description )
    liz.setProperty( "Artist_Genre", genre )
    liz.setProperty( "Artist_Style", style )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True, totalItems=items)
    return(u,liz,True)
        
def getParams():
    param=[]
    paramstring=sys.argv[2]
    if len(paramstring)>=2:
            params=sys.argv[2]
            cleanedparams=params.replace('?','')
            if (params[len(params)-1]=='/'):
                    params=params[0:len(params)-2]
            pairsofparams=cleanedparams.split('&')
            param={}
            for i in range(len(pairsofparams)):
                    splitparams={}
                    splitparams=pairsofparams[i].split('=')
                    if (len(splitparams))==2:
                            param[splitparams[0]]=splitparams[1]

    return param

params=getParams()

mode=None
pos=None
artistid=None
albumid=None


try:
    artistid=urllib.unquote_plus(params["artistid"])
except:
    pass
        
try:
    albumid=urllib.unquote_plus(params["albumid"])
except:
    pass
        
try:
    pos=urllib.unquote_plus(params["pos"])
except:
    pass
        
try:
    mode=int(params["mode"])
except:
    pass

"""
print "Mode: "     + str(mode)
print "ArtistID: " + str(artistid)
print "AlbumID: "  + str(albumid)
print "SongPos: "  + str(pos)
"""
xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Music-Library')

if mode==None or artistid==None:
    #print ""
    xbmcplugin.setContent(int(sys.argv[1]), 'artists')
    showArtists()
    xbmcplugin.setContent(int(sys.argv[1]), 'artists')

elif mode==1:
    #print ""+url
    xbmcplugin.setContent(int(sys.argv[1]), 'albums')
    showAlbums(artistid)
    xbmcplugin.setContent(int(sys.argv[1]), 'albums')

elif mode==2:
    #print ""+url
    xbmcplugin.setContent(int(sys.argv[1]), 'songs')
    showSongs(artistid, albumid)
    xbmcplugin.setContent(int(sys.argv[1]), 'songs')

elif mode==3:
    #print ""+url
    playSong(artistid, albumid, pos)