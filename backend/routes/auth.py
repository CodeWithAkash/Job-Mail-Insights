from flask import Blueprint, redirect, request, session, jsonify
from google_auth_oauthlib.flow import Flow
from config import Config
import os

auth_bp = Blueprint('auth', __name__)

def get_flow():
    return Flow.from_client_config(
        {
            "web": {
                "client_id": Config.GOOGLE_CLIENT_ID,
                "client_secret": Config.GOOGLE_CLIENT_SECRET,
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "redirect_uris": [Config.REDIRECT_URI]
            }
        },
        scopes=Config.SCOPES,
        redirect_uri=Config.REDIRECT_URI
    )

@auth_bp.route('/login')
def login():
    flow = get_flow()
    authorization_url, state = flow.authorization_url(
        access_type='offline',
        include_granted_scopes='true'
    )
    session['state'] = state
    return jsonify({'auth_url': authorization_url})

@auth_bp.route('/callback')
def callback():
    try:
        state = session.get('state')
        flow = get_flow()
        flow.fetch_token(authorization_response=request.url)
        
        credentials = flow.credentials
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Redirect to frontend with success
        return redirect(f"{Config.FRONTEND_URL}?auth=success")
    except Exception as e:
        return redirect(f"{Config.FRONTEND_URL}?auth=error&message={str(e)}")

@auth_bp.route('/status')
def auth_status():
    if 'credentials' in session:
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out successfully'})