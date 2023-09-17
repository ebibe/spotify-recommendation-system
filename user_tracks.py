from credentials import sp
import pandas as pd
import spotify_tracks as spotify_tracks
import sqlite3

if __name__ == "__main__":
    results = sp.current_user_top_tracks(limit=1000, offset=0,time_range='short_term') # Get the top 1000 songs from the user

    # Convert it to Dataframe
    track_name = []
    track_id = []
    artist = []
    album = []
    duration = []
    popularity = []
    for i, items in enumerate(results['items']):
        if items is not None:

            track_name.append(items['name'])
            track_id.append(items['id'])
            artist.append(items["artists"][0]["name"])
            duration.append(items["duration_ms"])
            album.append(items["album"]["name"])
            popularity.append(items["popularity"])



    # Create the final df
    df_favourite = pd.DataFrame({ "track_name": track_name,
                                 "album": album,
                                 "track_id": track_id,
                                 "artist": artist,
                                 "duration": duration,
                                 "popularity": popularity})

    print('test',df_favourite)



    # Getting track features for each song in favorite song dataframe
    fav_tracks = []
    batch_size = 50
    for i in range(0, len(df_favourite['track_id']), batch_size):
        batch = df_favourite['track_id'].iloc[i:i+batch_size]
        try:
            track = spotify_tracks.getTrackFeatures(batch)
            if track is not None:
                fav_tracks.extend(track)


        except Exception as e:
            print("Error fetching features for tracks:",batch)
            print("Error:", str(e))
            print(e)
            pass



    #for track in df_favourite['track_id']:
        #try:
            #track = spotify_tracks.getTrackFeatures(track)
            #fav_tracks.append(track)
        #except:
            #pass


    df_fav = pd.DataFrame(fav_tracks, columns = ['track_id', 'name', 'album', 'artist', 'release_date', 'length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature'])
    print("Number of rows in User_tracks DataFrame:", len(df_fav))
    print(df_fav)

    # Creating favorite column to use in classification
    df_fav['favorite'] = 1
    
    conn = sqlite3.connect('all.db') # creates a database connection



    df_fav.to_sql('user_songs', conn, if_exists='replace', index=False) # creates a table in the database
    print("Successfully created database connection with user_songs table")

    conn.close()
    print("Database connection closed")