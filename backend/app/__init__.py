from flask import Flask
from flask_cors import CORS
from app.config.settings import Config
from app.services.data_service import DataService
import logging

logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    CORS(app)
    
    # Initialize DataService and load Spotify data
    data_service = DataService()
    spotify_data = data_service.load_spotify_data()
    if spotify_data is None:
        logger.error("Failed to load Spotify data at startup")
    else:
        logger.info(f"Successfully loaded Spotify data with {len(spotify_data)} rows")
    
    # Register blueprints
    from app.routes.spotify_routes import spotify_bp
    app.register_blueprint(spotify_bp, url_prefix='/api')
    
    return app 