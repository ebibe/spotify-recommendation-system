import sqlite3
from credentials import sp
import pandas as pd


# Creating a function to get the first 50 tracks IDs from each spotify playlists
# Getting playlist IDs from each of Spotify's playlists
def get_playlist_ids(username):
    playlists = sp.user_playlists(username) # gets the playlists of the user 'spotify'
    playlist_ids = [] # list of playlist IDs
    while playlists: # while there are still playlists to get
        for i, playlist in enumerate(playlists['items']):
            playlist_ids.append(playlist['uri'][-22:])
        if playlists['next']: # if there are more playlists to get
            playlists = sp.next(playlists) # get the next set of playlists
        else: # if there are no more playlists to get
            playlists = None
    return playlist_ids

def getTrackIDs(playlist_id):
    ids = []

    print('il problema è accedere alle informazioni delle singole playlist')
    playlist = sp.playlist(playlist_id)

    for item in playlist['tracks']['items'][:50]: # only get the first 50 tracks
        track = item['track']
        if track is not None:
            #print(track['id'])
            ids.append(track['id'])

    return ids


# Creating a function to get the audio features for each track
def getTrackFeatures(track_ids):
    try:
        # Get track information

        information = sp.tracks(track_ids) #it makes a lot of requests to the API, NOT GOOD(50)
        features = sp.audio_features(track_ids)  # it makes a lot of requests to the API, NOT GOOD(100)
        if features:

            tracks_info = []
            for i, audio_features in enumerate(features):
                # Get the required track information
                name = information['tracks'][i]['name']
                album = information['tracks'][i]['album']['name']
                artist = information['tracks'][i]['album']['artists'][0]['name']
                release_date = information['tracks'][i]['album']['release_date']
                length = information['tracks'][i]['duration_ms']
                popularity = information['tracks'][i]['popularity']

                # Extract the specific audio features from the features_response

                acousticness = audio_features['acousticness']
                danceability = audio_features['danceability']
                energy = audio_features['energy']
                instrumentalness = audio_features['instrumentalness']
                liveness = audio_features['liveness']
                loudness = audio_features['loudness']
                speechiness = audio_features['speechiness']
                tempo = audio_features['tempo']
                time_signature = audio_features['time_signature']

                track_info = [track_ids[i], name, album, artist, release_date, length, popularity, danceability,
                              acousticness, energy, instrumentalness, liveness, loudness, speechiness, tempo,
                              time_signature]
                tracks_info.append(track_info)

            return tracks_info

        else:
            raise ValueError("No audio features found for track:", track_ids)



    except Exception as e:
        print("Error fetching features for track:", track_ids)
        print("Error:", str(e))
        return None


# Creating a function to get the first 50 tracks IDs from each spotify playlists
def fetch_spotify_data():

    # Step 0: Get playlist IDs
    playlist_ids = get_playlist_ids('spotify')
    print(f'numero di playlist di spotify prese: {len(playlist_ids)}')




    # Step 2: Fetch track IDs from the playlists
    track_ids = []
    for playlist_id in playlist_ids[:200]: # only get the first 200 playlists
        print("Fetching track ids for playlist:", playlist_id)
        try:
            track_ids.extend(getTrackIDs(playlist_id))
        except Exception as e:
            print("Error finding the spotify playlist:", playlist_id)
            print("Error:", str(e))
            continue

    #print(f'Numero di tracce totali prese dalle prime 200 playlist di spotify:{len(track_ids)}')

    # Step 3: Fetch track features
    tracks = []
    batch_size = 50

    for i in range(0, len(track_ids), batch_size): # get the track features in batches of 50
        batch_track_ids = track_ids[i:i + batch_size]
        try:
            #print("Fetching features for tracks:", batch_track_ids)
            batch_tracks = getTrackFeatures(batch_track_ids)
            if batch_tracks is not None:
                tracks.extend(batch_tracks)
            else:
                print("No features found for tracks:", batch_track_ids)

        except Exception as e:
            print("Error fetching features for tracks:", batch_track_ids)
            print("Error:", str(e))

    tracks = [track for track in tracks if track is not None] # remove any tracks that were not found (additional check)

    # Step 4: Create DataFrame
    df = pd.DataFrame(tracks, columns=['track_id', 'name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])

    # Step 5: Print the DataFrame or do further processing


    return df


#playlists = sp.user_playlists('spotify') # gets the playlists of the user 'spotify'
#spotify_playlist_ids = [] # list of playlist IDs
#while playlists: # while there are still playlists to get
    #for i, playlist in enumerate(playlists['items']):
       # spotify_playlist_ids.append(playlist['uri'][-22:])
    #if playlists['next']: # if there are more playlists to get
        #playlists = sp.next(playlists) # get the next set of playlists
    #else: # if there are no more playlists to get
        #playlists = None
#print(spotify_playlist_ids[:20])
#print(len(spotify_playlist_ids))
###

if __name__ == "__main__":

    df = fetch_spotify_data()


    print("Number of rows in Spotify_tracks DataFrame:", len(df))
    print(df)

    # Dropping columns that could lead to data leakage
    df = df.drop(columns=['name', 'album', 'artist', 'release_date'])

    # Dropping duplicated songs
    df = df.drop_duplicates(subset=['track_id'])

    # Creating favorite column to use in classification
    df['favorite'] = 0






    # Creating a database connection
    conn = sqlite3.connect('all.db') # creates a database connection


    df.to_sql('spotify_songs', conn, if_exists='replace', index=False) # creates a table in the database
    print("Successfully created database connection")

    conn.close()
    print("Database connection closed")