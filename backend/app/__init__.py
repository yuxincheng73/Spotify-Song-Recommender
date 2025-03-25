from flask import Flask
from flask_cors import CORS
from app.config.settings import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    
    # Register blueprints
    from app.routes.spotify_routes import spotify_bp
    app.register_blueprint(spotify_bp, url_prefix='/api')
    
    return app 