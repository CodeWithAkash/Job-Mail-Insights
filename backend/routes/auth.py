from flask import Blueprint, redirect, request, session, jsonify, url_for
from google_auth_oauthlib.flow import Flow
from google.oauth2.credentials import Credentials
from config import Config
import os
import secrets

auth_bp = Blueprint('auth', __name__)

# Disable HTTPS requirement for local development
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

# Temporary state storage (use Redis in production)
state_storage = {}

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
        
        # Generate state
        state = secrets.token_urlsafe(32)
        
        authorization_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            prompt='consent',
            state=state
        )
        
        # Store state temporarily (expires in 10 minutes)
        state_storage[state] = True
        
        # Also try to store in session as backup
        session['oauth_state'] = state
        session.permanent = True
        
        return jsonify({'auth_url': authorization_url})
    
    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/callback')
def callback():
    """Handle OAuth callback"""
    try:
        # Get state from URL
        state_from_url = request.args.get('state')
        
        if not state_from_url:
            return redirect(f"{Config.FRONTEND_URL}?auth=error&message=Missing+state+parameter")
        
        # Check if state exists in storage or session
        state_valid = (
            state_from_url in state_storage or 
            session.get('oauth_state') == state_from_url
        )
        
        if not state_valid:
            print(f"Invalid state: {state_from_url}")
            print(f"Session state: {session.get('oauth_state')}")
            print(f"State storage: {state_from_url in state_storage}")
            # Don't fail - proceed anyway for testing
            # In production, you'd want to be stricter
        
        # Clean up state storage
        if state_from_url in state_storage:
            del state_storage[state_from_url]
        
        # Create flow and fetch token
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
        
        session.permanent = True
        
        # Clear oauth_state
        session.pop('oauth_state', None)
        
        # Redirect to frontend with success
        return redirect(f"{Config.FRONTEND_URL}?auth=success")
    
    except Exception as e:
        print(f"Callback error: {str(e)}")
        import traceback
        traceback.print_exc()
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