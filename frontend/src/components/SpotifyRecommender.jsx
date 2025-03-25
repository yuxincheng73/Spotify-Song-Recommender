import React, { useState } from 'react';
import { Music, X, Save, List, User, LogOut } from 'lucide-react';

const SpotifyRecommender = () => {
  const [recommendations, setRecommendations] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [selectedPlaylist, setSelectedPlaylist] = useState('');
  const [showPlaylistDropdown, setShowPlaylistDropdown] = useState(false);
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showProfileDropdown, setShowProfileDropdown] = useState(false);

  // Different mock playlists for logged in vs demo users
  const mockPlaylists = isLoggedIn ? [
    { id: 1, name: "Workout Mix" },
    { id: 2, name: "Chill Vibes" },
    { id: 3, name: "Party Hits" },
    { id: 4, name: "Road Trip Songs" },
    { id: 5, name: "Study Focus" }
  ] : [
    { id: 1, name: "Demo Playlist 1" },
    { id: 2, name: "Demo Playlist 2" },
    { id: 3, name: "Demo Playlist 3" }
  ];

  const handleLogin = (e) => {
    e.preventDefault();
    setIsLoggedIn(true);
    setShowLoginModal(false);
    setSelectedPlaylist(''); // Reset selection when logging in
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setShowProfileDropdown(false);
    setSelectedPlaylist('');
    setRecommendations([]);
  };

  const generateRecommendations = () => {
    if (!selectedPlaylist) {
      alert('Please select a playlist first');
      return;
    }
    
    setIsLoading(true);
    setTimeout(() => {
      const mockSongs = [
        { id: 1, name: "Bohemian Rhapsody", artist: "Queen", album: "A Night at the Opera" },
        { id: 2, name: "Stairway to Heaven", artist: "Led Zeppelin", album: "Led Zeppelin IV" },
        { id: 3, name: "Hotel California", artist: "Eagles", album: "Hotel California" },
        { id: 4, name: "Sweet Child O' Mine", artist: "Guns N' Roses", album: "Appetite for Destruction" },
      ];
      setRecommendations(mockSongs);
      setIsLoading(false);
    }, 1500);
  };

  const handleSaveToSpotify = () => {
    if (!isLoggedIn) {
      setShowLoginModal(true);
    } else {
      alert('Saving to Spotify!');
    }
  };

  const removeSong = (songId) => {
    setRecommendations(recommendations.filter(song => song.id !== songId));
  };

  return (
    <div className="min-h-screen bg-dark-primary text-dark-text">
      {/* Login Modal */}
      {showLoginModal && (
        <div className="fixed inset-0 bg-black bg-opacity-70 backdrop-blur-sm flex items-center justify-center z-50">
          <div className="bg-dark-secondary rounded-lg p-8 w-96 relative border border-dark-accent">
            <button 
              onClick={() => setShowLoginModal(false)}
              className="absolute top-4 right-4 text-dark-text-secondary hover:text-dark-text"
            >
              <X className="w-5 h-5" />
            </button>
            <h2 className="text-2xl font-bold mb-6 text-dark-text">Login to Spotify</h2>
            <form onSubmit={handleLogin} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-dark-text-secondary mb-1">Username</label>
                <input 
                  type="text" 
                  className="w-full px-3 py-2 bg-dark-accent border border-dark-accent rounded-md 
                           focus:outline-none focus:ring-2 focus:ring-dark-spotify-green text-dark-text"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-dark-text-secondary mb-1">Password</label>
                <input 
                  type="password" 
                  className="w-full px-3 py-2 bg-dark-accent border border-dark-accent rounded-md 
                           focus:outline-none focus:ring-2 focus:ring-dark-spotify-green text-dark-text"
                  required
                />
              </div>
              <button 
                type="submit"
                className="w-full bg-dark-spotify-green text-white py-2 rounded-md 
                         hover:bg-dark-spotify-hover transition-colors duration-200"
              >
                Login
              </button>
            </form>
          </div>
        </div>
      )}

      {/* Header with Auth */}
      <div className="relative">
        <div className="absolute top-4 right-8">
          {!isLoggedIn ? (
            <button
              onClick={() => setShowLoginModal(true)}
              className="bg-dark-secondary text-dark-text px-4 py-2 rounded-lg 
                       shadow-lg hover:bg-dark-accent transition-colors duration-200"
            >
              Login
            </button>
          ) : (
            <div className="relative">
              <button
                onClick={() => setShowProfileDropdown(!showProfileDropdown)}
                className="w-10 h-10 rounded-full bg-dark-spotify-green flex items-center justify-center 
                         text-white hover:bg-dark-spotify-hover transition-colors duration-200"
              >
                <User className="w-5 h-5" />
              </button>
              
              {showProfileDropdown && (
                <div className="absolute right-0 mt-2 w-48 bg-dark-secondary rounded-lg shadow-lg py-2 z-50 
                              border border-dark-accent">
                  <button
                    onClick={handleLogout}
                    className="w-full px-4 py-2 text-left text-dark-text hover:bg-dark-accent 
                             flex items-center transition-colors duration-200"
                  >
                    <LogOut className="w-4 h-4 mr-2" />
                    Logout
                  </button>
                </div>
              )}
            </div>
          )}
        </div>

        {/* Main Content */}
        <div className="p-8">
          <div className="max-w-4xl mx-auto">
            {/* Header */}
            <div className="mb-8 text-center">
              <h1 className="text-4xl font-bold mb-4 text-dark-text">
                Enhanced Music Recommender
              </h1>
              <p className="text-dark-text-secondary mb-6">
                Discover new music tailored to your taste
              </p>
              
              {/* Button Container */}
              <div className="flex justify-center gap-4 mb-8">
                {/* Playlist Selector */}
                <div className="relative">
                  <button
                    onClick={() => setShowPlaylistDropdown(!showPlaylistDropdown)}
                    className="bg-dark-secondary text-dark-text px-6 py-3 rounded-lg font-medium 
                             shadow-lg hover:bg-dark-accent transition-colors duration-200 
                             flex items-center justify-center border border-dark-accent"
                  >
                    <List className="w-5 h-5 mr-2" />
                    {selectedPlaylist ? selectedPlaylist : 'Choose Playlist'}
                  </button>
                  
                  {showPlaylistDropdown && (
                    <div className="absolute mt-2 w-full bg-dark-secondary rounded-lg shadow-lg py-2 z-10 
                                  border border-dark-accent">
                      {mockPlaylists.map((playlist) => (
                        <button
                          key={playlist.id}
                          onClick={() => {
                            setSelectedPlaylist(playlist.name);
                            setShowPlaylistDropdown(false);
                          }}
                          className="w-full px-4 py-2 text-left hover:bg-dark-accent text-dark-text 
                                   transition-colors duration-200"
                        >
                          {playlist.name}
                        </button>
                      ))}
                    </div>
                  )}
                </div>

                {/* Generate Button */}
                <button
                  onClick={generateRecommendations}
                  disabled={isLoading}
                  className="bg-dark-spotify-green text-white px-6 py-3 rounded-lg font-medium 
                           shadow-lg hover:bg-dark-spotify-hover transition-colors duration-200 
                           flex items-center justify-center
                           disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  <Music className="w-5 h-5 mr-2" />
                  {isLoading ? 'Generating...' : 'Generate Recommendations'}
                </button>
              </div>
            </div>

            {/* Recommendations List */}
            {recommendations.length > 0 && (
              <div className="space-y-4">
                <div className="bg-dark-secondary rounded-xl shadow-md overflow-hidden border border-dark-accent">
                  {recommendations.map((song) => (
                    <div 
                      key={song.id}
                      className="p-4 flex items-center justify-between border-b border-dark-accent 
                               last:border-b-0 hover:bg-dark-accent transition-colors duration-150"
                    >
                      <div className="flex-1">
                        <h3 className="font-semibold text-dark-text">{song.name}</h3>
                        <p className="text-dark-text-secondary text-sm">
                          {song.artist} • {song.album}
                        </p>
                      </div>
                      <button
                        onClick={() => removeSong(song.id)}
                        className="ml-4 p-2 text-dark-text-secondary hover:text-red-500 
                                 hover:bg-red-500/10 rounded-full transition-colors duration-200"
                      >
                        <X className="w-5 h-5" />
                      </button>
                    </div>
                  ))}
                </div>

                {/* Save to Spotify Button */}
                <button
                  onClick={handleSaveToSpotify}
                  className="w-full bg-dark-spotify-green text-white px-6 py-3 rounded-lg 
                           font-medium shadow-lg hover:bg-dark-spotify-hover 
                           transition-colors duration-200 flex items-center justify-center"
                >
                  <Save className="w-5 h-5 mr-2" />
                  Save to Spotify
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SpotifyRecommender;