from flask_ask import statement, audio, question
from googmusic import ask, app, musicman, client, music_queue
from fuzzywuzzy import fuzz, process

@ask.launch
def login():
    text = 'Welcome to Goog Music ' \
           'Try asking me to play a song'
    prompt = 'For example say, play music by The Wet Secrets'
    return question(text).reprompt(prompt).simple_card(title='Welcome to GoogMusic!', content='Try asking me to play a song')

@ask.intent("GoogMusicPlaySongIntent")
def play_song(song_name, artist_name):
    print('Fetching song %s by %s' % (song_name, artist_name))

    song = musicman.get_song(song_name, artist_name)
    if song is False:
        return statement('Sorry, I couldn\' find that song')

    print('storeId', song['storeId'])

    stream_url = client.get_stream_url(song['storeId'])
    print(stream_url)

    return audio('Playing %s' % song_name).play(stream_url)

@ask.intent('GoogMusicPlayArtistIntent')
def play_artist(artist_name):
    print('Fetching songs by artist: %s' % artist_name)

    artist = musicman.get_artist(artist_name)

    artist_info = client.get_artist_info(artist, include_albums = False, max_top_tracks=25, max_rel_artist=0)
    top_tracks = artist_info['topTracks']

    if not top_tracks:
        return statement('I\'m sorry, I couldn\'t find that artist')

    music_queue = []
    for track in top_tracks:
        music_queue.append(track)

    return audio('Playing top 25 tracks by %s' % artist_info['name']).play(client.get_stream_url(music_queue.pop(0)['nid']))

@ask.intent('GoogMusicPlayGenreRadioIntent')
def play_genre_radio(genre_name):
    genres = client.get_genres()

    g_id = None

    for g in genres:
        if fuzz.partial_ratio(genre_name, g['name']) > 75:
            g_id = g['id']

    if g_id == None:
        return statement('Sorry, I couldn\'t find that genre')

    station = client.create_station(genre_name, genre_id=g_id)

    tracks = client.get_station_tracks(station, num_tracks=50)
    music_queue = []
    for track in tracks:
        music_queue.append(track)
        print(track['nid'])

    return audio('You have selected %s radio' % str(g_id)).play(client.get_stream_url(music_queue.pop(0)['nid']))
