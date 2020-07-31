import os
import requests
import json

from flask import Blueprint, request, redirect
from flask_login import login_required, login_user, logout_user
from oauthlib.oauth2 import WebApplicationClient

from extensions import db
from models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')


def _get_google_provider_cfg():
    return requests.get('https://accounts.google.com/.well-known/openid-configuration').json()


def _get_client():
    return WebApplicationClient(os.getenv('GOOGLE_CLIENT_ID'))


@bp.route('/login')
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = _get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg['authorization_endpoint']

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    client = _get_client()
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + '/callback',
        scope=['openid', 'email', 'profile'],
    )
    return redirect(request_uri)


@bp.route('/login/callback')
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get('code')

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = _get_google_provider_cfg()
    token_endpoint = google_provider_cfg['token_endpoint']

    # Prepare and send a request to get tokens! Yay tokens!
    client = _get_client()
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(
            os.getenv('GOOGLE_CLIENT_ID'),
            os.getenv('GOOGLE_CLIENT_SECRET'),
        )
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that you have tokens (yay) let's find and hit the URL
    # from Google that gives you the user's profile information,
    # including their Google profile image and email
    userinfo_endpoint = google_provider_cfg['userinfo_endpoint']
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    if not userinfo_response.json().get('email_verified'):
        return 'User email not available or not verified by Google.', 400

    rj = userinfo_response.json()

    # Doesn't exist? Add it to the database.
    user = User.query.get_user(rj['sub'])

    if not user:
        # Create a user in your db with the information provided
        # by Google
        user = User(
            google_user_id=rj['sub'],
            email=rj['email'],
            name=rj['given_name']
        )
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect('/')


@bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
