import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.services.spotify_service import SpotifyService
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
            logger.info("")
            
        return True
        
    except Exception as e:
        logger.error(f"Error testing get_playlist_tracks: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_get_playlist_tracks()
    if success:
        logger.info("Test completed successfully!")
    else:
        logger.error("Test failed!") 