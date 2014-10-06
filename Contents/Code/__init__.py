ART      = 'art-default.jpg'
ICON     = 'icon-default.png'

MP3_URL = 'http://mp3stream1.apasf.apa.at:8000'
#MP3_URL = 'http://stream-eu1.radioparadise.com:80/mp3-128'

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
    ObjectContainer.thumb = R(ICON)
    ObjectContainer.art = R(ART)
    ObjectContainer.view_group = 'List'

    DirectoryObject.thumb = R(ICON)

    TrackObject.thumb = R(ICON)
    TrackObject.art = R(ART)

####################################################################################################

@handler(PREFIX, 'FM4 Radio')
def MainMenu():
    oc = ObjectContainer(no_cache = True)

    # Fetch MP3 urls
    # Add playable TrackObject to menu structure
    oc.add(
        CreateTrackObject(
             mp3_url = MP3_URL,
	         title = 'FM4 Live'
        )
    )

    return oc

####################################################################################################
@route(PREFIX + '/CreateTrackObject', include_container = bool)
def CreateTrackObject(mp3_url, title, include_container = False):
    items = []

    if mp3_url:
        streams = [
            AudioStreamObject(
                codec = AudioCodec.MP3,
                channels = 2
            )
        ]

        items.append(
            MediaObject(
                container = Container.MP3,
                audio_codec = AudioCodec.MP3,
                audio_channels = 2,
                parts = [
                    PartObject(
                        key = Callback(PlayMP3, url = mp3_url),
                        streams = streams
                    )
                ]
            )
        )
        
    to = TrackObject(
            key = 
                Callback(
                    CreateTrackObject,
                    mp3_url = mp3_url,
                    title = title,
                    include_container = True
                ),
            rating_key = title,
            title = title,
            thumb = R(ICON),
            art = R(ART),
            items = items
    )
   
    if include_container:
        return ObjectContainer(objects = [to])
    else:
        return to
        
#################################################################################################### 
@route(PREFIX + '/PlayMP3.mp3')
def PlayMP3(url):
    return PlayAudio(url)
    
#################################################################################################### 
def PlayAudio(url):
    return Redirect(url)
