import pandas as pd
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DataService:
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / 'data' / 'spotify_data'
        self.spotify_data = None

    def load_spotify_data(self):
        """
        Load and parse the Spotify data CSV file.
        Returns a pandas DataFrame or None if there's an error.
        """
        try:
            csv_path = self.data_dir / 'spotify_data.csv'
            if not csv_path.exists():
                logger.error(f"Spotify data file not found at {csv_path}")
                return None

            self.spotify_data = pd.read_csv(csv_path)
            logger.info(f"Successfully loaded Spotify data with {len(self.spotify_data)} rows")
            return self.spotify_data

        except Exception as e:
            logger.error(f"Error loading Spotify data: {str(e)}")
            return None

    def get_data_summary(self):
        """
        Get a summary of the loaded Spotify data.
        """
        if self.spotify_data is None:
            return {"error": "Data not loaded"}

        try:
            return {
                "total_rows": len(self.spotify_data),
                "columns": list(self.spotify_data.columns),
                "summary_stats": self.spotify_data.describe().to_dict()
            }
        except Exception as e:
            logger.error(f"Error getting data summary: {str(e)}")
            return {"error": str(e)}

    def get_track_by_id(self, track_id):
        """
        Get track information by track ID.
        """
        if self.spotify_data is None:
            return {"error": "Data not loaded"}

        try:
            track = self.spotify_data[self.spotify_data['track_id'] == track_id]
            if track.empty:
                return {"error": "Track not found"}
            return track.iloc[0].to_dict()
        except Exception as e:
            logger.error(f"Error getting track by ID: {str(e)}")
            return {"error": str(e)} 