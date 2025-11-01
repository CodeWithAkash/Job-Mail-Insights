from flask import Flask, session
from flask_cors import CORS
from config import Config
from database import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    app.secret_key = Config.SECRET_KEY
    
    # Configure session
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to True in production with HTTPS
    
    # Enable CORS with credentials
    CORS(app, 
         resources={r"/api/*": {"origins": Config.FRONTEND_URL}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "OPTIONS"])
    
    # Register blueprints
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
    app.run(host='0.0.0.0', port=port, debug=True)