from flask import Blueprint, redirect, request, session, jsonify, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from config import Config
import os

auth_bp = Blueprint('auth', __name__)

# Disable HTTPS requirement for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

def get_flow():
    """Create OAuth flow instance"""
    client_config = {
        "web": {
            "client_id": Config.GOOGLE_CLIENT_ID,
            "client_secret": Config.GOOGLE_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [Config.REDIRECT_URI]
        }
    }
    
    flow = Flow.from_client_config(
        client_config,
        scopes=Config.SCOPES,
        redirect_uri=Config.REDIRECT_URI
    )
    
    return flow

@auth_bp.route('/login')
def login():
    """Initiate OAuth flow"""
    try:
        flow = get_flow()
        
        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent'
        )
        
        # Store state in session for CSRF protection
        session['state'] = state
        
        return jsonify({'auth_url': authorization_url})
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/callback')
def callback():
    """Handle OAuth callback"""
    try:
        # Verify state matches
        state = session.get('state')
        if not state:
            return redirect(f"{Config.FRONTEND_URL}?auth=error&message=Invalid state")
        
        # Create flow with same state
        flow = get_flow()
        flow.fetch_token(authorization_response=request.url)
        
        # Get credentials
        credentials = flow.credentials
        
        # Store credentials in session
        session['credentials'] = {
            'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes
        }
        
        # Clear state
        session.pop('state', None)
        
        # Redirect to frontend with success
        return redirect(f"{Config.FRONTEND_URL}?auth=success")
    
    except Exception as e:
        print(f"Callback error: {str(e)}")
        error_message = str(e).replace(' ', '+')
        return redirect(f"{Config.FRONTEND_URL}?auth=error&message={error_message}")

@auth_bp.route('/status')
def auth_status():
    """Check if user is authenticated"""
    if 'credentials' in session:
        return jsonify({'authenticated': True})
    return jsonify({'authenticated': False}), 401

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})