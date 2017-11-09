from flask_ask import statement, audio
from googmusic import ask

@ask.intent("AMAZON.PauseIntent")
def pause():
    return audio('Pausing').stop()
