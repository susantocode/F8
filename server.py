# /server.py

from functools import wraps
import json
from os import environ as env
from werkzeug.exceptions import HTTPException

from dotenv import load_dotenv, find_dotenv
from flask import Flask
from flask import jsonify
from flask import redirect
from flask import render_template
from flask import session
from flask import url_for
from authlib.flask.client import OAuth
from six.moves.urllib.parse import urlencode

app = Flask(__name__)

oauth = OAuth(app)

auth0 = oauth.register(
    'auth0',
    client_id='YOUR_CLIENT_ID',
    client_secret='YOUR_CLIENT_SECRET',
    api_base_url='https://YOUR_DOMAIN',
    access_token_url='https://YOUR_DOMAIN/oauth/token',
    authorize_url='https://YOUR_DOMAIN/authorize',
    client_kwargs={
        'scope': 'openid profile',
    },
)
# /server.py

# Here we're using the /callback route.
@app.route('/callback')
def callback_handling():
    # Handles response from token endpoint
    auth0.authorize_access_token()
    resp = auth0.get('userinfo')
    userinfo = resp.json()

    # Store the user information in flask session.
    session['jwt_payload'] = userinfo
    session['profile'] = {
        'user_id': userinfo['sub'],
        'name': userinfo['name'],
        'picture': userinfo['picture']
    }
    return redirect('/dashboard')
    # /server.py

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri='YOUR_CALLBACK_URL', audience='https://YOUR_DOMAIN/userinfo')
