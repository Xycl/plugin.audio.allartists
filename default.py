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

def playSong(artist, album, pos):
    # create a playlist
    playlist = xbmc.PlayList(0)
    # clear the playlist
    playlist.clear()
    counter=0

    json_request = '{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": { "sort": { "ignorearticle": true, "method": "track", "order": "ascending" }, "properties": ["file", "thumbnail", "fanart", "track", "rating", "duration", "album", "artist", "genre", "year", "comment"], "filter": {"and": [{"operator": "contains", "field": "artist", "value": "'+artist+'"}, {"operator": "contains", "field": "album", "value": "'+album+'"}]}}, "id": "libSongs"}'
    
    json_songs = xbmc.executeJSONRPC(json_request)
    result = json.loads(json_songs)
    
    if result["result"] != None:
        songs = result["result"]["songs"]

        for content in songs:
            liz = makeListItem(content["label"], content["thumbnail"], content["fanart"], content["track"], content["rating"]-48, content["duration"], content["album"], content["artist"], content["genre"], content["year"], content["comment"])
            playlist.add( content["file"], liz )
            counter=counter+1

        xbmc.executeJSONRPC('{"jsonrpc": "2.0", "method": "Player.Open", "params": { "item": { "playlistid": 0, "position" : '+ pos +' } }, "id": 1 }')

def makeListItem(label, thumbnail, fanart, track, rating, duration, album, artist, genre, year, comment):
    liz=xbmcgui.ListItem( label, iconImage="DefaultFolder.png", thumbnailImage=thumbnail)
    liz.setInfo( type="music", infoLabels={ "title": label, "tracknumber": track, "rating": str(rating) , "duration": duration, "album":album, "artist":artist, "genre": genre, "year":year, "comment":comment } )
    liz.setProperty( "Fanart_Image", fanart )
    return liz
    
def showSongs(artist, album):

    counter=0

    json_request = '{"jsonrpc": "2.0", "method": "AudioLibrary.GetSongs", "params": { "sort": { "ignorearticle": true, "method": "track", "order": "ascending" }, "properties": ["file", "thumbnail", "fanart", "track", "rating", "duration", "album", "artist", "genre", "year", "comment"], "filter": {"and": [{"operator": "contains", "field": "artist", "value": "'+artist+'"}, {"operator": "contains", "field": "album", "value": "'+album+'"}]}}, "id": "libSongs"}'

    json_songs = xbmc.executeJSONRPC(json_request)
    result = json.loads(json_songs)

    if result.get("result", None) != None:
        songs = result["result"]["songs"]
        for content in songs:
            listitem = addSong(content["label"]
                             , str(counter)
                             , 3
                             , content["thumbnail"]
                             , content["fanart"]
                             , content["track"] if "track" in content else ""
                             , content["rating"]-48
                             , content["duration"]
                             , content["album"]
                             , artist
                             , content["genre"] if "genre" in content else ""
                             , content["year"] if "year" in content else ""
                             , content["comment"] if "comment" in content else ""
                             , content["file"])
            counter=counter+1

        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TRACKNUM)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_TITLE_IGNORE_THE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_SONG_RATING)
    

def addSong(name, pos, mode, iconimage, fanart, track, rating, duration, album, artist, genre, year, comment, file):
    u=sys.argv[0]+"?artist="+urllib.quote_plus(artist.encode('utf-8'))+"&album="+urllib.quote_plus(album.encode('utf-8'))+"&pos="+str(pos)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))
    ok=True
    liz=xbmcgui.ListItem(artist + " - " + name, artist, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="music", infoLabels={ "title": name, "tracknumber": track, "rating": str(rating), "duration": duration, "album":album, "artist":artist, "genre": genre, "year":year, "comment":comment } )
    liz.setProperty( "Fanart_Image", fanart )
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok
        
def showAlbums(artist):
    json_request = '{"jsonrpc": "2.0", "method": "AudioLibrary.GetAlbums", "params": { "filter" : {"artist": "' + artist + '"}, "limits": { "start" : 0, "end": 50 }, "properties": ["playcount", "artist", "genre", "rating", "thumbnail", "fanart", "year", "mood", "style"], "sort": { "order": "ascending", "method": "album", "ignorearticle": true } }, "id": "libAlbums"}'

    json_album = xbmc.executeJSONRPC(json_request)
    result = json.loads(json_album)
    
    if result.get("result", None) != None and "albums" in result["result"]:
        albums = result["result"]["albums"]
        for content in albums:
            addAlbums(content["label"]
                       , artist
                       , content["label"]
                       , 2
                       , content["thumbnail"]
                       , content["fanart"]
                       , content["year"] if "year" in content else ""
                       , content["genre"] if "genre" in content else "")
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_ALBUM_IGNORE_THE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE)
        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_DATE)


def addAlbums(name, artist, album, mode, iconimage, fanart, date, genre):
    u=sys.argv[0]+"?artist="+urllib.quote_plus(artist.encode('utf-8'))+"&album="+urllib.quote_plus(album.encode('utf-8'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))

    ok=True
    if str(date) == "0":
        datum = " "
    else:
        datum = str(date)

    liz=xbmcgui.ListItem(label=artist +" - "+name, label2=artist, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="music", infoLabels={ "album": name , "year":date, "genre": genre,"artist":artist, "title": name, "Title": artist} )
    liz.setProperty( "Fanart_Image", fanart )
    liz.setLabel2(datum)
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)

        
def showArtists():
    json_request= '{"jsonrpc": "2.0", "method": "AudioLibrary.GetArtists", "params": {"properties": ["thumbnail", "fanart", "genre", "description", "style"], "albumartistsonly": false, "sort": { "ignorearticle": true, "method": "artist", "order": "ascending" } }, "id": 1}'
    
    json_artists = xbmc.executeJSONRPC(json_request)
    result = json.loads(json_artists)

    if result["result"] != None and "artists" in result["result"]:
        artists = result["result"]["artists"]
        totalitems = len(artists)
        for content in artists:
            addArtists(content["label"]
                                        , content["artist"]
                                        , 1
                                        , content["thumbnail"]
                                        , content["fanart"]
                                        , content["description"] if "description" in content else ""
                                        , content["genre"] if "genre" in content else ""
                                        , content["style"] if "style" in content else ""
                                        , totalitems)


        xbmcplugin.addSortMethod(int(sys.argv[1]), xbmcplugin.SORT_METHOD_ARTIST_IGNORE_THE)




def addArtists(name, artist, mode, iconimage, fanart, description, genres, styles, items):
    u=sys.argv[0]+"?artist="+urllib.quote_plus(artist.encode('utf-8'))+"&mode="+str(mode)+"&name="+urllib.quote_plus(name.encode('utf-8'))

    ok=True
    liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo( type="music", infoLabels={ "artist": name } )
    try:
        if fanart != None:
            liz.setProperty( "Fanart_Image", fanart)
    except:
        pass
    try:
        if description != None:
            liz.setProperty( "Artist_Description", description )
    except:
        pass
    
    try:
        if genres != None:
            for genre in genres:
                if genre != None and genre != "":
                    liz.setProperty( "Artist_Genre", genre )
    except:
        pass    
    
    try:
        if styles != None:
            for style in styles:
                if style != None and style != "":
                    liz.setProperty( "Artist_Style", style )
    except:
        pass    
    
    ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True, totalItems=items)
        
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
artist=None
album=None


try:
    artist=urllib.unquote_plus(params["artist"])
except:
    pass
        
try:
    album=urllib.unquote_plus(params["album"])
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


xbmcplugin.setPluginCategory(int(sys.argv[1]), 'Music-Library')

if mode==None or artist==None:
    xbmcplugin.setContent(int(sys.argv[1]), 'artists')
    showArtists()

elif mode==1:
    xbmcplugin.setContent(int(sys.argv[1]), 'albums')
    showAlbums(artist)

elif mode==2:
    xbmcplugin.setContent(int(sys.argv[1]), 'songs')
    showSongs(artist, album)

elif mode==3:
    playSong(artist, album, pos)
    
xbmcplugin.endOfDirectory(int(sys.argv[1]))    