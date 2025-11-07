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
    app.config['SESSION_COOKIE_SAMESITE'] = 'None'
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    
    # Enable CORS with credentials
    CORS(app, 
         resources={r"/api/*": {"origins": Config.FRONTEND_URL}},
         supports_credentials=True,
         allow_headers=["Content-Type", "Authorization"],
         methods=["GET", "POST", "OPTIONS"],
         expose_headers=["Content-Type", "Authorization"])
    
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
    # Use threaded=False and processes=1 for Windows stability
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False
    )