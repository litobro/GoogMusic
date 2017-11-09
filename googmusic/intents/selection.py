from flask_ask import statement, audio, question
from googmusic import ask, app, musicman, client

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
