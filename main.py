from flask import Flask
from flask_ask import Ask, question, statement, convert_errors, audio
from youtube_dl import YoutubeDL

ip = '127.0.0.1' # SYSTEM IP
host = 'localhost'  # doesn't require anything else since we're using ngrok
port = 5000  # may want to check and make sure this port isn't being used by anything else


ytdl_options = {
	'format': 'bestaudio/best',
	'restrictfilenames': False,
	'noplaylist': False,
	'nocheckcertificate': True,
	'ignoreerrors': False,
	'logtostderr': False,
	'quiet': True,
	'no_warnings': True,
	'default_search': 'auto',
	'source_address': ip
}
ytdl = YoutubeDL(ytdl_options)
app = Flask(__name__)
ask = Ask(app, '/alexa_youtube')


@ask.launch
def launch():
	return question('Say an artist and/or song name')


@ask.session_ended
def session_ended():
	return "{}", 200


@ask.intent('AMAZON.StopIntent')
def handle_stop_intent():
	return statement('Okay')


@ask.intent('AMAZON.PauseIntent')
def handle_pause_intent():
	return audio('Stopping music').stop()


@ask.intent('AMAZON.FallbackIntent')
def handle_fallback_intent():
	return question('you have to start your command with play, search, or look for')


@ask.intent('QueryIntent', mapping={'query': 'Query'})
def handle_query_intent(query):

	if not query or 'query' in convert_errors:
		return question('Say an artist and/or song name')

	data = ytdl.extract_info(f"ytsearch:{query}", download=False)
	search_results = data['entries']

	if not search_results:
		return question('no results found, try another search query')

	result = search_results[0]
	song_name = result['title']
	channel_name = result['uploader']

	for format_ in result['formats']:
		if format_['ext'] == 'm4a':
			mp3_url = format_['url']
			return audio(f'now playing {song_name} by {channel_name}').play(mp3_url)

	return question('no results found, try another search query')


app.run(host=host, port=port)
