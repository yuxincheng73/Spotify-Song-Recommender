from flask import Blueprint, jsonify, request
from app.services.spotify_service import SpotifyService
import logging

logger = logging.getLogger(__name__)
spotify_bp = Blueprint('spotify', __name__)
spotify_service = SpotifyService()

@spotify_bp.route('/recommendations')
def get_recommendations():
    try:
        limit = request.args.get('limit', default=10, type=int)
        
        if limit < 1 or limit > 50:
            return jsonify({
                "error": "Invalid limit parameter. Must be between 1 and 50."
            }), 400

        recommendations = spotify_service.get_recommendations(limit)
        return jsonify({
            "recommendations": recommendations,
            "total": len(recommendations)
        })

    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@spotify_bp.route('/top-songs')
def get_top_songs():
    try:
        top_songs = spotify_service.get_top_songs()
        return jsonify({
            "top_songs": top_songs,
            "total": len(top_songs)
        })

    except Exception as e:
        logger.error(f"Error in top-songs endpoint: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@spotify_bp.route('/top-playlists')
def get_top_playlists():
    try:
        top_playlists = spotify_service.get_top_playlists()
        return jsonify({
            "top_playlists": top_playlists,
            "total": len(top_playlists)
        })

    except Exception as e:
        logger.error(f"Error in top-playlists endpoint: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@spotify_bp.route('/callback')
def callback():
    try:
        spotify_service.handle_callback(request.args.get('code'))
        return "Authentication successful! You can close this window."
    except Exception as e:
        logger.error(f"Error in callback: {str(e)}")
        return f"Authentication failed: {str(e)}" 