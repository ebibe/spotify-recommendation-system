# Spotify Recommendation System

A machine learning-based music recommendation system that analyzes Spotify playlist songs and user preferences to provide personalized music recommendations.

## 🎵 Overview

This system uses Spotify's Web API to collect audio features from songs in public playlists and compares them with a user's top tracks to build a recommendation model. The system learns from the user's music preferences and can predict whether they would like new songs based on audio characteristics.

## 🚀 Features

- **Data Collection**: Automatically fetches songs from Spotify's public playlists
- **User Preference Analysis**: Analyzes user's top tracks to understand musical taste
- **Audio Feature Extraction**: Extracts 11 audio features including:
  - Danceability
  - Energy
  - Acousticness
  - Instrumentalness
  - Liveness
  - Loudness
  - Speechiness
  - Tempo
  - Time Signature
  - Popularity
  - Valence
- **Machine Learning Model**: Builds a classification model to predict song preferences
- **Database Storage**: Stores all data in SQLite for efficient retrieval

## 📁 Project Structure

```
spotify-recommendation-system/
├── spotify_tracks.py          # Collects songs from Spotify playlists
├── user_tracks.py            # Fetches and processes user's top tracks
├── model_creation.ipynb      # Model training and analysis notebook
├── credentials.py            # Spotify API credentials (not tracked)
└── all.db                   # SQLite database (generated)
```

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/ebibe/spotify-recommendation-system.git
   cd spotify-recommendation-system
   ```

2. **Install required packages**
   ```bash
   pip install pandas numpy scikit-learn spotipy sqlite3 seaborn matplotlib imbalanced-learn
   ```

3. **Set up Spotify API credentials**
   - Create a Spotify Developer account at [developer.spotify.com](https://developer.spotify.com)
   - Create a new app and get your Client ID and Client Secret
   - Create a `credentials.py` file with your Spotify API setup:
   ```python
   import spotipy
   from spotipy.oauth2 import SpotifyOAuth
   
   sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
       client_id="your_client_id",
       client_secret="your_client_secret",
       redirect_uri="http://localhost:8080",
       scope="user-top-read"
   ))
   ```

## 🎯 Usage

### 1. Collect Spotify Playlist Data
```bash
python spotify_tracks.py
```
This script will:
- Fetch songs from Spotify's public playlists
- Extract audio features for each song
- Store the data in `all.db` database

### 2. Collect User's Top Tracks
```bash
python user_tracks.py
```
This script will:
- Fetch your top tracks from Spotify
- Extract audio features for your favorite songs
- Store them in the database with a "favorite" label

### 3. Train the Model
Open and run `model_creation.ipynb` in Jupyter Notebook:
```bash
jupyter notebook model_creation.ipynb
```
This notebook will:
- Load data from the database
- Perform exploratory data analysis
- Train a machine learning model
- Evaluate model performance

## 📊 How It Works

1. **Data Collection Phase**
   - Collects songs from the first 200 Spotify playlists
   - Extracts up to 50 songs per playlist
   - Fetches user's top 1000 tracks

2. **Feature Engineering**
   - Extracts 11 audio features per song
   - Labels user's top tracks as "favorites" (1)
   - Labels playlist songs as "non-favorites" (0)

3. **Model Training**
   - Uses SMOTE to handle class imbalance
   - Trains a classification model
   - Evaluates performance using various metrics

4. **Recommendation**
   - Predicts likelihood of user liking new songs
   - Recommends songs with high prediction scores

## 🔧 Configuration

The system can be configured by modifying the following parameters:

- **Number of playlists**: Change `playlist_ids[:200]` in `spotify_tracks.py`
- **Songs per playlist**: Modify `[:50]` in `getTrackIDs()` function
- **User tracks limit**: Adjust `limit=1000` in `user_tracks.py`
- **Batch size**: Modify `batch_size = 50` for API efficiency

## 📈 Model Performance

The system uses various machine learning techniques:
- **Imbalanced Learning**: SMOTE for handling skewed data
- **Feature Selection**: Uses audio features for prediction
- **Classification**: Binary classification (like/dislike)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## ⚠️ Important Notes

- **API Limits**: Be mindful of Spotify's API rate limits
- **Credentials**: Never commit your `credentials.py` file
- **Data Privacy**: Ensure user data is handled responsibly
- **Dependencies**: Make sure all required packages are installed

## 🔮 Future Enhancements

- Add more sophisticated recommendation algorithms
- Implement collaborative filtering
- Add a web interface for easier interaction
- Include playlist generation features
- Add more audio features and metadata

## 📞 Support

If you encounter any issues or have questions, please:
1. Check the existing issues
2. Create a new issue with detailed description
3. Include error messages and system information

---

**Built with ❤️ using Python and Spotify Web API**
