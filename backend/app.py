from flask import Flask, jsonify, request
from flask_cors import CORS
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Initialize Spotify client with OAuth
spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
    redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI', 'http://localhost:5000/callback'),
    scope='user-top-read playlist-read-private user-read-recently-played'
))

@app.route('/api/recommendations')
def get_recommendations():
    try:
        # Get the number of recommendations from query parameters
        limit = request.args.get('limit', default=10, type=int)
        
        # Validate limit parameter
        if limit < 1 or limit > 50:
            return jsonify({
                "error": "Invalid limit parameter. Must be between 1 and 50."
            }), 400

        # Get recommendations using Spotify's API
        # Using some default seed tracks for demonstration
        results = spotify.recommendations(
            seed_tracks=['0c6xIDDpzE81m2q797ordA'],  # Example seed tracks
            seed_artists=['4NHQUGzhtTLFvgF5SZesLK'],
            seed_genres=['classical', 'country'],
            limit=limit
        )

        # Format the response
        recommendations = []
        for track in results['tracks']:
            recommendations.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            })

        return jsonify({
            "recommendations": recommendations,
            "total": len(recommendations)
        })

    except Exception as e:
        logger.error(f"Error in recommendations endpoint: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/top-songs')
def get_top_songs():
    try:
        logger.debug("Attempting to get top tracks")
        
        # Check if we have a valid token
        if not spotify.auth_manager.get_cached_token():
            logger.error("No valid token found")
            return jsonify({
                "error": "Authentication required. Please authenticate with Spotify first."
            }), 401

        # Get top tracks from Spotify's API
        results = spotify.current_user_top_tracks(limit=5)
        logger.debug(f"Received results: {results}")

        # Format the response
        top_songs = []
        for track in results['items']:
            top_songs.append({
                'name': track['name'],
                'artist': track['artists'][0]['name'],
                'album': track['album']['name'],
                'duration_ms': track['duration_ms'],
                'popularity': track['popularity'],
                'preview_url': track['preview_url'],
                'external_url': track['external_urls']['spotify']
            })

        return jsonify({
            "top_songs": top_songs,
            "total": len(top_songs)
        })

    except Exception as e:
        logger.error(f"Error in top-songs endpoint: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/api/top-playlists')
def get_top_playlists():
    try:
        logger.debug("Attempting to get top playlists")
        
        # Check if we have a valid token
        if not spotify.auth_manager.get_cached_token():
            logger.error("No valid token found")
            return jsonify({
                "error": "Authentication required. Please authenticate with Spotify first."
            }), 401

        # Get recently played tracks first
        recently_played = spotify.current_user_recently_played(limit=50)
        playlist_play_counts = {}  # Dictionary to store playlist play counts

        # Count how many times each playlist appears in recently played
        for item in recently_played['items']:
            if 'context' in item and item['context'] and item['context']['type'] == 'playlist':
                playlist_id = item['context']['uri'].split(':')[-1]
                playlist_play_counts[playlist_id] = playlist_play_counts.get(playlist_id, 0) + 1

        # Get all user playlists
        results = spotify.current_user_playlists(limit=50)
        for playlist in results['items']:
            logger.debug(f"Found playlist: {playlist['name']}")

        # Create a list of playlists with their play counts
        playlist_data = []
        for playlist in results['items']:
            playlist_id = playlist['id']
            play_count = playlist_play_counts.get(playlist_id, 0)
            playlist_data.append({
                'playlist': playlist,
                'play_count': play_count
            })

        # Sort playlists by play count (most played first)
        playlist_data.sort(key=lambda x: x['play_count'], reverse=True)

        # Take top 5 most played playlists
        top_playlists = []
        for item in playlist_data[:5]:
            playlist = item['playlist']
            top_playlists.append({
                'name': playlist['name'],
                'description': playlist['description'],
                'tracks_total': playlist['tracks']['total'],
                'external_url': playlist['external_urls']['spotify'],
                'images': playlist['images'],
                'owner': playlist['owner']['display_name'],
                'play_count': item['play_count']
            })

        return jsonify({
            "top_playlists": top_playlists,
            "total": len(top_playlists)
        })

    except Exception as e:
        logger.error(f"Error in top-playlists endpoint: {str(e)}")
        return jsonify({
            "error": str(e)
        }), 500

@app.route('/callback')
def callback():
    try:
        # Handle the OAuth callback
        spotify.auth_manager.get_access_token(request.args.get('code'))
        return "Authentication successful! You can close this window."
    except Exception as e:
        logger.error(f"Error in callback: {str(e)}")
        return f"Authentication failed: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True) 