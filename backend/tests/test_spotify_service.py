import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.spotify_service import SpotifyService
from app.services.data_service import DataService
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_get_playlist_tracks():
    try:
        # Initialize Spotify service
        spotify_service = SpotifyService()
        
        # Test with a known playlist ID (you can replace this with your own playlist ID)
        playlist_id = "5bEEmQXkVYOuDhz2nQJcCn"  # Remove spotify:playlist: prefix
        
        logger.info(f"Testing get_playlist_tracks with playlist ID: {playlist_id}")
        
        # Get playlist tracks
        playlist_data = spotify_service.get_playlist_tracks(playlist_id)
        
        # Print playlist information
        logger.info(f"Playlist Name: {playlist_data['playlist_name']}")
        logger.info(f"Playlist Description: {playlist_data['playlist_description']}")
        logger.info(f"Total Tracks: {playlist_data['total_tracks']}")
        
        # Print first 5 tracks as sample
        logger.info("\nSample Tracks (First 5):")
        for track in playlist_data['tracks'][:5]:
            logger.info(f"- {track['name']} by {track['artist']}")
            logger.info(f"  Album: {track['album']}")
            logger.info(f"  Duration: {track['duration_ms']}ms")
            logger.info(f"  Popularity: {track['popularity']}")
            logger.info(f"  Spotify URL: {track['external_url']}")
            logger.info(f"  Added at: {track['added_at']}")
            logger.info(f"  URI: {track['uri']}")
            logger.info(f"  Preview URL: {track['preview_url']}")
            # Audio features
            logger.info(f"  Audio Features:")
            logger.info(f"    Danceability: {track.get('danceability', 'N/A')}")
            logger.info(f"    Energy: {track.get('energy', 'N/A')}")
            logger.info(f"    Key: {track.get('key', 'N/A')}")
            logger.info(f"    Loudness: {track.get('loudness', 'N/A')}")
            logger.info(f"    Mode: {track.get('mode', 'N/A')}")
            logger.info(f"    Speechiness: {track.get('speechiness', 'N/A')}")
            logger.info(f"    Acousticness: {track.get('acousticness', 'N/A')}")
            logger.info(f"    Instrumentalness: {track.get('instrumentalness', 'N/A')}")
            logger.info(f"    Liveness: {track.get('liveness', 'N/A')}")
            logger.info(f"    Valence: {track.get('valence', 'N/A')}")
            logger.info(f"    Tempo: {track.get('tempo', 'N/A')}")
            logger.info(f"    Time Signature: {track.get('time_signature', 'N/A')}")
            logger.info("")
            
        return True
        
    except Exception as e:
        logger.error(f"Error testing get_playlist_tracks: {str(e)}")
        return False

def test_load_spotify_data():
    try:
        # Initialize Data service
        data_service = DataService()
        
        logger.info("Testing load_spotify_data...")
        
        # Load the data
        data = data_service.load_spotify_data()
        
        if data is None:
            logger.error("Failed to load Spotify data")
            return False
            
        # Log basic information about the loaded data
        logger.info(f"Successfully loaded {len(data)} rows of data")
        logger.info(f"Columns in the dataset: {', '.join(data.columns)}")
        
        # Log the first 10 rows
        logger.info("\nFirst 10 rows of data:")
        for index, row in data.head(10).iterrows():
            logger.info(f"\nRow {index + 1}:")
            for column in data.columns:
                logger.info(f"  {column}: {row[column]}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error testing load_spotify_data: {str(e)}")
        return False

def test_audio_features():
    try:
        # Initialize Spotify service
        spotify_service = SpotifyService()
        
        # Log authentication status
        logger.info("Checking authentication status...")
        try:
            current_user = spotify_service.spotify.current_user()
            logger.info(f"Successfully authenticated as: {current_user['display_name']}")
            logger.info(f"User ID: {current_user['id']}")
        except Exception as e:
            logger.error(f"Authentication check failed: {str(e)}")
            return False
        
        # Test with a known playlist ID that has tracks with audio features
        playlist_id = "5bEEmQXkVYOuDhz2nQJcCn"
        
        logger.info("Testing audio features retrieval...")
        
        # Get playlist tracks
        playlist_data = spotify_service.get_playlist_tracks(playlist_id)
        
        # Verify that we have tracks
        assert len(playlist_data['tracks']) > 0, "No tracks found in playlist"
        
        # Check first track for audio features
        first_track = playlist_data['tracks'][0]
        
        # Log track ID for debugging
        logger.info(f"Testing audio features for track: {first_track['name']} (ID: {first_track['id']})")
        
        # Try to get audio features directly for this track
        try:
            direct_features = spotify_service.spotify.audio_features([first_track['id']])
            logger.info(f"Direct API call result: {direct_features}")
        except Exception as e:
            logger.error(f"Error in direct API call: {str(e)}")
            logger.error("This might be an authentication issue. Please check your Spotify credentials and scopes.")
            return False
        
        # Verify that audio features are present and have valid values
        audio_features = [
            'danceability', 'energy', 'key', 'loudness', 'mode',
            'speechiness', 'acousticness', 'instrumentalness',
            'liveness', 'valence', 'tempo', 'time_signature'
        ]
        
        for feature in audio_features:
            assert feature in first_track, f"Missing audio feature: {feature}"
            assert first_track[feature] is not None, f"Audio feature {feature} is None"
            assert first_track[feature] != 'N/A', f"Audio feature {feature} is 'N/A'"
            
            # Log the feature value
            logger.info(f"Track '{first_track['name']}' - {feature}: {first_track[feature]}")
        
        # Verify value ranges for numeric features
        logger.info(f"Danceability: {first_track['danceability']} (should be between 0 and 1)")
        logger.info(f"Energy: {first_track['energy']} (should be between 0 and 1)")
        logger.info(f"Speechiness: {first_track['speechiness']} (should be between 0 and 1)")
        logger.info(f"Acousticness: {first_track['acousticness']} (should be between 0 and 1)")
        logger.info(f"Instrumentalness: {first_track['instrumentalness']} (should be between 0 and 1)")
        logger.info(f"Liveness: {first_track['liveness']} (should be between 0 and 1)")
        logger.info(f"Valence: {first_track['valence']} (should be between 0 and 1)")
        logger.info(f"Tempo: {first_track['tempo']} (should be positive)")
        logger.info(f"Time signature: {first_track['time_signature']} (should be positive)")
        
        logger.info("Audio features test completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error testing audio features: {str(e)}")
        return False

if __name__ == "__main__":
    # Run all tests
    spotify_test_success = test_get_playlist_tracks()
    data_test_success = test_load_spotify_data()
    audio_features_success = test_audio_features()
    
    if spotify_test_success and data_test_success and audio_features_success:
        logger.info("All tests completed successfully!")
    else:
        logger.error("Some tests failed!") 