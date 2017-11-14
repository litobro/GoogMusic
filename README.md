# GoogMusic
A Google Music Alexa Skill

This is a rewrite of the popular GeeMusic Alexa Skill from scratch. It borrows heavily from the original skill but is written entirely from scratch. Born out of a frustration with how complicated it was to get the original skill running and certain bugs that were noticed.

This project is still in development and subject to a lot of change. Basic functionality is working at this time. You are required to run this script on your own server. I personally recommend a cheap VPS or local machine which can be exposed to the web. 

### Notes
**This skill is not made or endorsed by Google or the original makers of GeeMusic.** This skill uses the [gmusicapi](https://github.com/simon-weber/gmusicapi) by [Simon Weber](https://simon.codes) and is dependent on it as a library.

### Supported Languages
This sill is developed exclusively on an Amazon **Echo Dot** used in Canada set to **English(US)**. I make no promises or guarentees of compatibility with other versions or setups. 

## Features
This script is used by saying "Alexa, tell Geemusic to...". Some of the search terms use fuzzy string logic so feel free to experiment. I encourage looking at the sample utterances for samples of what to say.

Currently we have implemented:
```
Play song Never Gonna Give You Up
Play the song Radioactive by Imagine Dragons

Play music by The Wet Secrets
Play artist Metric
Play songs by Sam Roberts Band

Start genre radio for Indie
Play Rock radio
Start radio for genre Country
```

You can currently also say "Alexa pause" to stop playback and "Alexa resume" to resume playback.

### Roadmap
A lot of things honestly. Probably get all of the existing functionality in the old GeeMusic skill implemented and then a bit more. I've currently implemented my #1 need which was to play a radio station as background music.

## Setup
The following setup has been tested on Ubuntu 16.04 Xenial on a virtual private server. It should be functional on other UNIX type environments. 

### Start a local development server
This server must be running at all times and the webserver involved must also be run at all times. That is outside the scope of this article, I recommend looking into options such as 'screen' or 'circus' for running jobs in the background with monitoring.

Begin by cloning the repository to your server:

```bash
$ git clone https://github.com/litobro/GoogMusic.git
```

Ensure you have Python 3 installed and `cd` into the directory. I highly recommend running this script inside of a virtual environment. 

```bash
# Run this to create a virtual environment and activate it
$ python3 -m venv .
$ source bin/activate

# Continue here, or begin here to skip creating a virtual environment
$ pip3 install -r requirements.txt
```

This may take some time, allow the requirements to install, it is required to setup a configuration file after it has completed. Also in the root of the directory create a file called `config.py` using `touch config.py`. It should contain these variables:

```
# Google Credentials
GOOGLE_EMAIL='YOUR EMAIL HERE'
GOOGLE_PASSWORD='YOUR PASSWORD HERE'

ANDROID_ID='A VALID AND REGISTERED MOBILE_DEVICE ID HERE'
```

As with the original GeeMusic skill, I *highly recommend* you enable 2-factor authentication on your Google Account and insert an application specific password. The password will unfortunately at this time be stored in plaintext on your server. 

Your Android_ID can be extracted from your google music webpage which shows registered devices. Simply inspect each device listed in your web browser and view the source, the ID will make itself evident in the list. 

### Run the local development server
At this time, you can try running the server using `python3 server.py`. It should launch without issue using flask. 

## Create the development Skill on Amazon

Open up the [Alexa Dashboard](https://developer.amazon.com/edw/home.html), click "Get Started" in the **Alexa Skills Kit** box. Then click on the yellow "Add a New Skill" button in the top right corner.

Going through the various sections

### Skill Information

| Field | Value |
| ----- | ----- |
| Skill Type | Custom Interaction Model |
| Language | Select US English |
| Name | GoogMusic |
| Invocation Name | gee music |
| Audio Player | Yes |

### Interaction model

On the "Interaction Model" step, paste in the contents of `speech_assets/intent_schema.json` to the intent schema field and the contents of `speech_assets/sample_utterances.txt` to the sample utterances field.

### Configuration

We'll point our skill at the URL for our development server. Select HTTPS as the endpoint type and enter your server's URL in the corresponding box. Remember that your development server must be publicly accessible AND using HTTPS in order for Amazon to be able to connect/interact with it.

If your development server is running on a server that is already available on the internet, type its URL (such as `https://geemusic.example.com/alexa`). Make sure you include the `/alexa`, otherwise this won't work!

If you are running the server on a computer behind a firewall we'll need to expose the server via a tunnel in order for this to work. I usually use [ngrok](https://ngrok.com/) for these situations and have used it to develop this project. To start a tunnel run `ngrok http 5001` in a console window. You should then see a few URLs, one of which being a publicly accessible HTTPS link to your development server. Copy this URL, being sure to append `/alexa` so the final result looks something like `https://[some-code].ngrok.io/alexa`. 

You'll also want to select "No" for the "Account Linking" field before moving on.

### SSL Certificate

If using [ngrok](https://ngrok.com/) or [heroku](https://heroku.com) select the second option "My development endpoint is a subdomain of a domain that has a wildcard certificate from a certificate authority."

### Test

Scroll down to the "Service Simulator" section, the check the Skill is talking to Alexa correcty enter the word help  _"help"_ then click "Ask Gee Music", and you'll ideally see some resulting JSON in the Service Response box. You can then try testing phrases like `Play artist Arctic Monkeys`

### Publishing Information, Privacy & Compliance

Do not fill these in and make sure you never click "SUBMIT FOR CERTIFICATION". You are NOT submitting the Skill to Amazon to include in the public Skill store.  
