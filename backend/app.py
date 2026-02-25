from flask import Flask
from flask_cors import CORS
from flask_session import Session
from config import Config
import os
from datetime import timedelta

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    
    # ✅ Session configuration for cross-domain
    # Since backend is on onrender.com and frontend on akash-codes.space,
    # we CANNOT use domain-based cookies. Use server-side sessions instead.
    app.config.update(
        SESSION_TYPE='filesystem',  # Store sessions on server
        SESSION_PERMANENT=True,
        SESSION_USE_SIGNER=True,
        SESSION_COOKIE_NAME='jobmail_session',
        SESSION_COOKIE_SAMESITE='None',  # Allow cross-site
        SESSION_COOKIE_SECURE=True,       # HTTPS only
        SESSION_COOKIE_HTTPONLY=True,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7)
    )
    
    # Initialize server-side sessions
    Session(app)
    
    # ✅ Allowed frontend origins
    allowed_origins = [
        "https://jobmail.akash-codes.space",
        "http://localhost:3000"
    ]
    
    # ✅ CORS configuration
    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True,
        allow_headers=["Content-Type", "Authorization"],
        expose_headers=["Content-Type", "Set-Cookie"]
    )
    
    # ✅ Register blueprints
    from routes.auth import auth_bp
    from routes.emails import emails_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(emails_bp, url_prefix='/api')
    
    @app.route('/')
    def index():
        return {
            'message': 'JobMail Insight API',
            'status': 'running',
            'version': '1.0.0'
        }
    
    @app.route('/health')
    def health():
        return {'status': 'healthy', 'database': 'mongodb'}
    
    return app

if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )