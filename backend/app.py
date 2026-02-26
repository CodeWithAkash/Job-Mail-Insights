from flask import Flask
from flask_session import Session
from flask_cors import CORS
from config import Config
import os
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY

    # -----------------------------
    # SERVER-SIDE SESSION CONFIG
    # -----------------------------
    app.config.update(
        SESSION_TYPE='filesystem',                 # Store sessions on server
        SESSION_PERMANENT=True,
        SESSION_USE_SIGNER=True,
        SESSION_FILE_DIR='/tmp/flask_session',     # Render-safe temp dir
        SESSION_COOKIE_NAME='session',
        SESSION_COOKIE_SAMESITE='None',
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        PERMANENT_SESSION_LIFETIME=timedelta(days=7)
    )
    # Initialize Flask-Session
    Session(app)

    # -----------------------------
    # CORS CONFIG
    # -----------------------------
    allowed_origins = [
        "https://jobmail.akash-codes.space",
        "http://localhost:3000"
    ]

    CORS(
        app,
        resources={r"/api/*": {"origins": allowed_origins}},
        supports_credentials=True
    )

    # -----------------------------
    # REGISTER BLUEPRINTS
    # -----------------------------
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