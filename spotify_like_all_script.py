import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def get_user_playlists():
    limit = 50
    offset = 0
    playlists = []

    while True:
        res = sp.current_user_playlists(limit=limit, offset=offset)
        if not res['items']:
            break

        for playlist in res['items']:
            is_radio = 'radio' in playlist['name'].lower()

            if not is_radio:
                playlists.append(playlist['id'])

        offset += limit

    return playlists    

def get_songs_from_playlists(playlists):
    songs = []

    print("Fetching Data")

    for idx, playlist in enumerate(playlists):
        progress = round((idx + 1) / len(playlists) * 100)
        print(str(progress) + '% ' + "." * progress, end='\r')

        uri = 'spotify:playlist:' + playlist
        res = sp.playlist_tracks(uri);

        for song in res['items']:
            songs.append(song['track']['id'])

    return songs

def extract_current_likes():
    limit = 20
    offset = 0
    tracks = []

    while True:
        res = sp.current_user_saved_tracks(limit=limit, offset=offset, market=None)
        if not res['items']:
            break

        for item in res['items']:
            tracks.append(item['track']['id'])

        offset += limit

    return tracks

def dislike_songs(songs):
    if not songs:
        return
    
    for song in songs:
        sp.current_user_saved_tracks_delete(tracks=[song])


def like_songs(new_songs):
    if not new_songs:
        return
    
    for song in new_songs:
        sp.current_user_saved_tracks_add(tracks=[song])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--id', '-i', type=str, help="client id")
    parser.add_argument('--secret', '-s', type=str, help="client secret")
    parser.add_argument('--remove-old', '-r', action='store_true', help="To remove previous liked songs")
    parser.add_argument('--new-user', '-u', action='store_true', help="Remove old user cache")

    args = parser.parse_args()

    client_id = args.id
    client_secret = args.secret

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback', scope='playlist-read-private user-library-read user-library-modify'))

    if args.remove_old:
        print("Remove Songs")
        liked_songs = extract_current_likes()      
        dislike_songs(liked_songs)  
    
    playlists = get_user_playlists()
    
    new_songs = get_songs_from_playlists(playlists)

    like_songs(new_songs)

    print("Done ✅")
