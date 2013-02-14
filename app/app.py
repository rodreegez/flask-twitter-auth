import os
import yaml

from flask import Flask, url_for, render_template, session
from flask_oauth import OAuth

app = Flask(__name__)

oauth = OAuth()

try:
  with open('app/config.yml', 'r') as config:
    y =  yaml.load(config)
    os.environ['TWITTER_CONSUMER_KEY']    = y['TWITTER_CONSUMER_KEY']
    os.environ['TWITTER_CONSUMER_SECRET'] = y['TWITTER_CONSUMER_SECRET']
except IOError as e:
  print "config.yml not found. Assuming ENV vars set elsewhere"

twitter = oauth.remote_app('twitter',
    base_url          = 'https://api.twitter.com/1/',
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url  = 'https://api.twitter.com/oauth/access_token',
    authorize_url     = 'https://api.twitter.com/oauth/authenticate',
    consumer_key      = os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret   = os.environ['TWITTER_CONSUMER_SECRET']
)

@app.route('/')
def index():
  user = { 'nickname': 'Rodreegez' }
  return render_template('index.html', user = user)

@app.route('/login')
def login():
  return


if __name__ == '__main__':
  app.run(debug=True)
