from flask import Flask
from flask_cors import CORS
from config import Config
from database import db
import os
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # ✅ Session configuration for cross-domain (frontend + backend)
    app.config.update(
        SESSION_COOKIE_SAMESITE='None',
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_DOMAIN='.akash-codes.space',  # shared for subdomains
        PERMANENT_SESSION_LIFETIME=timedelta(days=7),
        SESSION_TYPE='filesystem'
    )

    # ✅ Correct frontend origins for CORS
    allowed_origins = [
        "https://jobmail.akash-codes.space",  # production frontend
        "http://localhost:3000"               # local dev frontend
    ]

    CORS(
        app,
        resources={r"/api/*": {
            "origins": allowed_origins,
            "supports_credentials": True,
            "allow_headers": ["Content-Type", "Authorization"],
            "expose_headers": ["Content-Type", "Authorization"],
            "methods": ["GET", "POST", "OPTIONS"]
        }},
        supports_credentials=True
    )

    # ✅ Register blueprints
    from routes.auth import auth_bp
    from routes.emails import emails_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(emails_bp, url_prefix='/api')

    # ✅ Health and root routes
    @app.route('/')
    def index():
        return {
            'message': 'JobMail Insight API',
            'status': 'running',
            'version': '1.0.0'
        }

    @app.route('/api/health')
    def health():
        return {'status': 'healthy', 'database': 'connected'}

    # ✅ CORS headers for OPTIONS preflight requests
    @app.after_request
    def after_request(response):
        origin = os.getenv('FRONTEND_URL', 'https://jobmail.akash-codes.space')
        if origin in allowed_origins:
            response.headers.add('Access-Control-Allow-Origin', origin)
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS,DELETE,PUT')
        return response

    return app


if __name__ == '__main__':
    app = create_app()
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )
