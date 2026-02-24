from flask import Flask
from flask_cors import CORS
from config import Config
import os
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # ✅ Proper session configuration for subdomain authentication
    app.config.update(
        SESSION_COOKIE_NAME='session',
        SESSION_COOKIE_DOMAIN='.akash-codes.space',  # Share across subdomains
        SESSION_COOKIE_SAMESITE='None',              # Required for cross-site cookies
        SESSION_COOKIE_SECURE=True,                  # Required for SameSite=None (HTTPS only)
        SESSION_COOKIE_HTTPONLY=True,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7)
    )

    # ✅ Allowed frontend origins
    allowed_origins = [
        "https://jobmail.akash-codes.space",
        "http://localhost:3000"
    ]

    # ✅ Correct CORS configuration (NO manual headers)
    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True
    )

    # ✅ Register blueprints
    from routes.auth import auth_bp
    from routes.emails import emails_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(emails_bp, url_prefix='/api')

    # Root route
    @app.route('/')
    def index():
        return {
            'message': 'JobMail Insight API',
            'status': 'running',
            'version': '1.0.0'
        }

    # Health check
    @app.route('/api/health')
    def health():
        return {
            'status': 'healthy',
            'database': 'connected'
        }

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )