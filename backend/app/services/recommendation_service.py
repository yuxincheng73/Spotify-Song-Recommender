import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class RecommendationService:
    def __init__(self, spotify_data):
        self.spotify_data = spotify_data
        self.vectorizer = TfidfVectorizer()
        
    def _prepare_track_features(self, track):
        """Prepare track features for similarity calculation."""
        # Text features
        text_features = [
            track['name'],
            track['artist'],
            track.get('album', ''),  # Using get() with default value in case album is missing
        ]
        
        # Numeric features normalized to strings
        numeric_features = [
            f"duration:{track['duration_ms']}",
            f"popularity:{track['popularity']}",
            f"danceability:{track.get('danceability', 0)}",
            f"energy:{track.get('energy', 0)}",
            f"key:{track.get('key', 0)}",
            f"loudness:{track.get('loudness', 0)}",
            f"mode:{track.get('mode', 0)}",
            f"speechiness:{track.get('speechiness', 0)}",
            f"acousticness:{track.get('acousticness', 0)}",
            f"instrumentalness:{track.get('instrumentalness', 0)}",
            f"liveness:{track.get('liveness', 0)}",
            f"valence:{track.get('valence', 0)}",
            f"tempo:{track.get('tempo', 0)}",
            f"time_signature:{track.get('time_signature', 4)}"
        ]
        
        return ' '.join(text_features + numeric_features)
    
    def _calculate_similarity(self, playlist_tracks, limit=10):
        """Calculate similarity between playlist tracks and dataset tracks."""
        try:
            # Prepare playlist tracks features
            playlist_features = [self._prepare_track_features(track) for track in playlist_tracks]
            
            # Prepare dataset tracks features
            dataset_features = self.spotify_data.apply(
                lambda row: self._prepare_track_features({
                    'name': row['track_name'],
                    'artist': row['artist_name'],
                    'album': row.get('album_name', ''),
                    'duration_ms': row['duration_ms'],
                    'popularity': row['popularity'],
                    'danceability': row.get('danceability', 0),
                    'energy': row.get('energy', 0),
                    'key': row.get('key', 0),
                    'loudness': row.get('loudness', 0),
                    'mode': row.get('mode', 0),
                    'speechiness': row.get('speechiness', 0),
                    'acousticness': row.get('acousticness', 0),
                    'instrumentalness': row.get('instrumentalness', 0),
                    'liveness': row.get('liveness', 0),
                    'valence': row.get('valence', 0),
                    'tempo': row.get('tempo', 0),
                    'time_signature': row.get('time_signature', 4)
                }), axis=1
            ).tolist()
            
            # Combine all features for vectorization
            all_features = playlist_features + dataset_features
            
            # Create TF-IDF matrix
            tfidf_matrix = self.vectorizer.fit_transform(all_features)
            
            # Calculate cosine similarity between playlist tracks and dataset tracks
            playlist_matrix = tfidf_matrix[:len(playlist_features)]
            dataset_matrix = tfidf_matrix[len(playlist_features):]
            
            # Calculate average similarity for each dataset track
            similarities = cosine_similarity(dataset_matrix, playlist_matrix)
            avg_similarities = np.mean(similarities, axis=1)
            
            # Get top similar tracks
            top_indices = np.argsort(avg_similarities)[-limit:][::-1]
            
            # Format recommendations
            recommendations = []
            for idx in top_indices:
                track = self.spotify_data.iloc[idx]
                recommendations.append({
                    'name': track['track_name'],
                    'artist': track['artist_name'],
                    'album': track.get('album_name', ''),
                    'duration_ms': track['duration_ms'],
                    'popularity': track['popularity'],
                    'danceability': track.get('danceability', 0),
                    'energy': track.get('energy', 0),
                    'key': track.get('key', 0),
                    'loudness': track.get('loudness', 0),
                    'mode': track.get('mode', 0),
                    'speechiness': track.get('speechiness', 0),
                    'acousticness': track.get('acousticness', 0),
                    'instrumentalness': track.get('instrumentalness', 0),
                    'liveness': track.get('liveness', 0),
                    'valence': track.get('valence', 0),
                    'tempo': track.get('tempo', 0),
                    'time_signature': track.get('time_signature', 4),
                    'similarity_score': float(avg_similarities[idx])
                })
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            raise
    
    def get_playlist_recommendations(self, playlist_tracks, limit=10):
        """Get recommendations based on playlist tracks."""
        try:
            recommendations = self._calculate_similarity(playlist_tracks, limit)
            return recommendations
        except Exception as e:
            logger.error(f"Error getting playlist recommendations: {str(e)}")
            raise 