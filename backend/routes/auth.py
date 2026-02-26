from flask import Blueprint, redirect, request, session, jsonify
from google_auth_oauthlib.flow import Flow
from config import Config
import secrets

auth_bp = Blueprint('auth', __name__)

def get_flow():
    client_config = {
        "web": {
            "client_id": Config.GOOGLE_CLIENT_ID,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [Config.REDIRECT_URI]
        }
    }

    return Flow.from_client_config(
        client_config,
        scopes=Config.SCOPES,
        redirect_uri=Config.REDIRECT_URI
    )

@auth_bp.route('/login')
def login():
    flow = get_flow()

    state = secrets.token_urlsafe(32)

    authorization_url, _ = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true',
        prompt='consent',
        state=state
    )

    session['oauth_state'] = state
    session.permanent = True

    return redirect(authorization_url)

@auth_bp.route('/callback')
def callback():
    try:
        state_from_url = request.args.get('state')

        if not state_from_url:
            return redirect("https://jobmail.akash-codes.space")

        if session.get('oauth_state') != state_from_url:
            session.clear()
            return redirect("https://jobmail.akash-codes.space")

        flow = get_flow()
        flow.fetch_token(authorization_response=request.url)

        credentials = flow.credentials

        session.clear()
        session['authenticated'] = True
        session['token'] = credentials.token
        session.permanent = True

        return redirect("https://jobmail.akash-codes.space")

    except Exception as e:
        print("Callback error:", str(e))
        session.clear()
        return redirect("https://jobmail.akash-codes.space")

@auth_bp.route('/status')
def auth_status():
    print("SESSION INSIDE STATUS:", dict(session))
    print("SESSION INSIDE CALLBACK:", dict(session))
    if session.get('authenticated'):
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})