from flask_ask import statement, audio
from googmusic import ask, music_queue, client

@ask.intent('AMAZON.CancelIntent')
def cancel():
    return audio().stop()

@ask.intent("AMAZON.PauseIntent")
def pause():
    return audio('Pausing').stop()

@ask.intent("AMAZON.ResumeIntent")
def resume():
    return audio('Resuming').resume()

@ask.on_playback_nearly_finished()
def nearly_finished():
    if len(music_queue) > 0:
        next_id = music_queue.pop(0)['nid']

        stream = client.get_stream_url(next_id)

        return audio().enqueue(stream)
