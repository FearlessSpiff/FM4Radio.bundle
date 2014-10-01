ART      = 'art-default.jpg'
ICON     = 'icon-default.png'

#MP3_URL = 'http://mp3stream1.apasf.apa.at:8000'
MP3_URL = 'http://stream-eu1.radioparadise.com:80/mp3-128'

METADATA_URL = 'http://radioparadise.com/ajax_xml_song_info.php?song_id=now'

PREFIX = '/music/FM4Radio'

####################################################################################################

# This function is initially called by the PMS framework to initialize the plugin. This includes
# setting up the Plugin static instance along with the displayed artwork.
def Start():
    # Initialize the plugin
    Plugin.AddViewGroup('List', viewMode = 'List', mediaType = 'items')
    Plugin.AddViewGroup('InfoList', viewMode = 'InfoList', mediaType = 'items')

    # Setup the artwork associated with the plugin
    ObjectContainer.title1 = 'Radio FM4'
    ObjectContainer.art = R(ART)
    ObjectContainer.view_group = 'List'

    DirectoryObject.thumb = R(ICON)

    TrackObject.thumb = R(ICON)
    TrackObject.art = R(ART)

####################################################################################################

@handler(PREFIX, 'FM4 Radio')
def MainMenu():
    oc = ObjectContainer(no_cache = True)

    song_info = XML.ObjectFromURL(METADATA_URL)

    # Fetch MP3 urls
    # Add playable TrackObject to menu structure
    oc.add(
        CreateTrackObject(
	     title = 'FM4 Live',
             artist = 'FM4',
             album = '',
             rating = float(song_info.rating.text),
             thumb = song_info.large_cover.text,
             art = song_info.image.large_url.text,
             mp3_url = MP3_URL
        )
    )

    return oc

####################################################################################################
@route(PREFIX + '/CreateTrackObject', rating = float, include_container = bool) 
def CreateTrackObject(title, artist, album, rating, thumb, art, mp3_url, include_container=False):        

    track_object = TrackObject(
        key = 
            Callback(
                CreateTrackObject,
                title = title,
                artist = artist,
                album = album,
                rating = rating,
                thumb = thumb,
                art = art,
                mp3_url = mp3_url,
                include_container = True
            ),
        rating_key = title,
        title = title,
        artist = artist,
        album = album,
        rating = rating,
        thumb = thumb,
        art = art
    )
    
    track_object.add(
        MediaObject(
            container = Container.MP3,
            audio_codec = AudioCodec.MP3,
            audio_channels = 2,
            bitrate = 128,
            parts = [
                PartObject(
                    key = Callback(PlayMP3, url = mp3_url)
                )
            ]
        )
    )
    
    if include_container:
        return ObjectContainer(objects=[track_object])
    else:
        return track_object
        
#################################################################################################### 
@route(PREFIX + '/PlayMP3.mp3')
def PlayMP3(url):
    return PlayAudio(url)
    
#################################################################################################### 
def PlayAudio(url):
    return Redirect(url)
