import spotipy
from spotipy.oauth2 import SpotifyOAuth
from app.config.settings import Config
import logging

logger = logging.getLogger(__name__)

class SpotifyService:
    def __init__(self):
        self.spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            client_id=Config.SPOTIFY_CLIENT_ID,
            client_secret=Config.SPOTIFY_CLIENT_SECRET,
            redirect_uri=Config.SPOTIFY_REDIRECT_URI,
            scope=Config.SPOTIFY_SCOPES
        ))

    def get_recommendations(self, limit=10):
        try:
            results = self.spotify.recommendations(
                seed_tracks=['0c6xIDDpzE81m2q797ordA'],
                seed_artists=['4NHQUGzhtTLFvgF5SZesLK'],
                seed_genres=['classical', 'country'],
                limit=limit
            )

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

            return recommendations
        except Exception as e:
            logger.error(f"Error getting recommendations: {str(e)}")
            raise

    def get_top_songs(self, limit=5):
        try:
            results = self.spotify.current_user_top_tracks(limit=limit)
            
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

            return top_songs
        except Exception as e:
            logger.error(f"Error getting top songs: {str(e)}")
            raise

    def get_top_playlists(self, limit=5):
        try:
            # Get recently played tracks
            recently_played = self.spotify.current_user_recently_played(limit=50)
            playlist_play_counts = {}

            # Count playlist plays
            for item in recently_played['items']:
                if 'context' in item and item['context'] and item['context']['type'] == 'playlist':
                    playlist_id = item['context']['uri'].split(':')[-1]
                    playlist_play_counts[playlist_id] = playlist_play_counts.get(playlist_id, 0) + 1

            # Get all playlists
            results = self.spotify.current_user_playlists(limit=50)
            
            # Create playlist data with play counts
            playlist_data = []
            for playlist in results['items']:
                playlist_id = playlist['id']
                play_count = playlist_play_counts.get(playlist_id, 0)
                playlist_data.append({
                    'playlist': playlist,
                    'play_count': play_count
                })

            # Sort by play count
            playlist_data.sort(key=lambda x: x['play_count'], reverse=True)

            # Format top playlists
            top_playlists = []
            for item in playlist_data[:limit]:
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

            return top_playlists
        except Exception as e:
            logger.error(f"Error getting top playlists: {str(e)}")
            raise

    def handle_callback(self, code):
        try:
            return self.spotify.auth_manager.get_access_token(code)
        except Exception as e:
            logger.error(f"Error handling callback: {str(e)}")
            raise

    def get_playlist_tracks(self, playlist_id):
        try:
            # Get playlist details
            playlist = self.spotify.playlist(playlist_id)
            
            # Get all tracks from the playlist
            tracks = []
            offset = 0
            limit = 100  # Maximum allowed by Spotify API
            
            while True:
                results = self.spotify.playlist_tracks(
                    playlist_id,
                    offset=offset,
                    limit=limit
                )
                
                for item in results['items']:
                    track = item['track']
                    if track:  # Check if track exists (not None)
                        tracks.append({
                            'name': track['name'],
                            'artist': track['artists'][0]['name'],
                            'album': track['album']['name'],
                            'duration_ms': track['duration_ms'],
                            'popularity': track['popularity'],
                            'preview_url': track['preview_url'],
                            'external_url': track['external_urls']['spotify'],
                            'added_at': item['added_at']
                        })
                
                # Check if there are more tracks to fetch
                if len(results['items']) < limit:
                    break
                    
                offset += limit
            
            return {
                'playlist_name': playlist['name'],
                'playlist_description': playlist['description'],
                'total_tracks': len(tracks),
                'tracks': tracks
            }
            
        except Exception as e:
            logger.error(f"Error getting playlist tracks: {str(e)}")
            raise 