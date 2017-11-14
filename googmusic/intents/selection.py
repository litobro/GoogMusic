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

@ask.intent('GoogMusicPlayGenreRadioIntent')
def play_genre_radio(genre_name):
    genres = client.get_genres()

    g_id = None

    for g in genres:
        #print(g['name'])
        if fuzz.partial_ratio(genre_name, g['name']) > 75:
            #print(genre_name, 'close to', g['name'])
            g_id = g['id']

    station = client.create_station(genre_name, genre_id=g_id)

    tracks = client.get_station_tracks(station, num_tracks=50)
    for track in tracks:
        music_queue.append(track)
        print(track['nid'])

    return audio('You have selected %s' % str(g_id)).play(client.get_stream_url(music_queue.pop(0)['nid']))
