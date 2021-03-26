from flask import Flask, render_template, request, url_for, flash, redirect, Response
from pygtail import Pygtail
from flask_ask import Ask, question, statement, convert_errors, audio
from youtube_dl import YoutubeDL
from werkzeug.exceptions import abort
import sqlite3
import logging
import datetime
import os
import sys
import time

ip = '0.0.0.0'  # System Ip
host = '0.0.0.0'  # doesn't require anything else since we're using ngrok
port = 5000  # may want to check and make sure this port isn't being used by anything else

LOG_FILE = 'app.log'
log = logging.getLogger('__name__')
logging.basicConfig(filename=LOG_FILE, level=logging.DEBUG)

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn


def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        abort(404)
    return post


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
app.config["DEBUG"] = os.environ.get("FLASK_DEBUG", True)
app.config["JSON_AS_ASCII"] = False
app.config['SECRET_KEY'] = 'dev'
app.config.from_mapping(
        BASE_URL="http://localhost:5000",
)

port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000
if app.config.get("ENV") == "development" and app.config["USE_NGROK"]:
        # pyngrok will only be installed, and should only ever be initialized, in a dev environment
        from pyngrok import ngrok

        # Get the dev server port (defaults to 5000 for Flask, can be overridden with `--port`
        # when starting the server
        port = sys.argv[sys.argv.index("--port") + 1] if "--port" in sys.argv else 5000
        ngrok.set_auth_token(os.environ['token'])
        token = os.environ['token']

        # Open a ngrok tunnel to the dev server
        public_url = ngrok.connect(port).public_url
        print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/progress')
def progress():
    def generate():
        x = 0
        while x <= 100:
            yield "data:" + str(x) + "\n\n"
            x = x + 10
            time.sleep(0.5)
    return Response(generate(), mimetype= 'text/event-stream')

@app.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)',
                         (title, content))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/delete', methods=('GET',))
def delete(id):
    post = get_post(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM posts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(post['title']))
    return redirect(url_for('index'))


@app.route('/log')
def progress_log():
	def generate():
		for line in Pygtail(LOG_FILE, every_n=1):
			yield "data:" + str(line) + "\n\n"
			time.sleep(0.5)
	return Response(generate(), mimetype= 'text/event-stream')

@app.route('/env')
def show_env():
	log.info("route =>'/env' - hit")
	env = {}
	for k,v in request.environ.items(): 
		env[k] = str(v)
	log.info("route =>'/env' [env]:\n%s" % env)
	return env

@app.route("/logs", methods=["GET"])
def logstream():
    return render_template('logs.html')


ask = Ask(app, '/alexa_youtube')

logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    return question('Say an artist and/or song name')


@ask.session_ended
def session_ended():
    return "{}", 200


@ask.intent('AMAZON.StopIntent')
def handle_stop_intent():
    return statement('Okay')


@ask.intent('AMAZON.CancelIntent')
def handle_stop_intent():
    return statement('Okay')


@ask.intent('AMAZON.PauseIntent')
def handle_pause_intent():
    return audio('Stopping music').stop()


@ask.intent('AMAZON.ResumeIntent')
def resume():
    return audio('Resuming.').resume()


@ask.intent('AMAZON.FallbackIntent')
def handle_fallback_intent():
    return question('you have to start your command with play, search, or look for')


@ask.intent('AMAZON.HelpIntent')
def handle_help_intent():
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


@app.route('/<int:post_id>')
def post(post_id):
    post = get_post(post_id)
    return render_template('post.html', post=post)


@app.route('/<int:id>/edit', methods=('GET', 'POST'))
def edit(id):
    post = get_post(id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']

        if not title:
            flash('Title is required!')
        else:
            conn = get_db_connection()
            conn.execute('UPDATE posts SET title = ?, content = ?'
                         ' WHERE id = ?',
                         (title, content, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', post=post)


app.run(host=host, port=port)
# Code by AndrewsTech and minecrosters
