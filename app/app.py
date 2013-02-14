import os
import yaml

from flask import Flask, url_for, render_template, session, redirect, request, flash
from flask_oauth import OAuth

app   = Flask(__name__)
oauth = OAuth()

# Load config variables
try:
  with open('app/config.yml', 'r') as config:
    y =  yaml.load(config)
    os.environ['TWITTER_CONSUMER_KEY']    = y['TWITTER_CONSUMER_KEY']
    os.environ['TWITTER_CONSUMER_SECRET'] = y['TWITTER_CONSUMER_SECRET']
    os.environ['APPLICATION_SECRET']      = y['APPLICATION_SECRET']
except IOError as e:
  print "config.yml not found. Assuming ENV vars set elsewhere"

# Set the application secret
app.secret_key = os.environ['APPLICATION_SECRET']

# Set up twitter OAuth client
twitter = oauth.remote_app('twitter',
    base_url          = 'https://api.twitter.com/1/',
    request_token_url = 'https://api.twitter.com/oauth/request_token',
    access_token_url  = 'https://api.twitter.com/oauth/access_token',
    authorize_url     = 'https://api.twitter.com/oauth/authenticate',
    consumer_key      = os.environ['TWITTER_CONSUMER_KEY'],
    consumer_secret   = os.environ['TWITTER_CONSUMER_SECRET']
)

# returns a tuple of twitter tokens, if they exist
@twitter.tokengetter
def get_twitter_token(token=None):
  return session.get('twitter_token')

# Routes
@app.route('/')
def index():
  if 'twitter_user' in session:
    return render_template('index.html', user = { 'nickname': session['twitter_user'] })
  return render_template('index.html', user = { 'nickname': 'Guest' })

@app.route('/login')
def login():
  return twitter.authorize(callback = url_for('oauth_authorized',
    next = request.args.get('next') or request.referrer or None))

@app.route('/oauth_authorized')
@twitter.authorized_handler
def oauth_authorized(resp):
  next_url = request.args.get('next') or url_for('index')
  if resp is None:
    flash('BOO')
    return redirect(next_url)

  print resp

  session['twitter_token'] = (
    resp['oauth_token'],
    resp['oauth_token_secret']
  )
  session['twitter_user'] = resp['screen_name']

  flash ('you were signed in as %s' % resp['screen_name'])
  return redirect(next_url)

# RUN THE TRACK!
if __name__ == '__main__':
  app.run(debug=True)
