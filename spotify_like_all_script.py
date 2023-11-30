import argparse
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm

def get_user_playlists():
    limit = 50
    offset = 0
    playlists = []
    total_playlists = None

    while True:
        res = sp.current_user_playlists(limit=limit, offset=offset)
        
        if total_playlists is None:
            total_playlists = res['total']
            progress_bar = tqdm(total=total_playlists, desc="Fetching Playlists", unit="playlist")

        if not res['items']:
            if len(playlists) == 0:
                print("No playlists found")
                
            break

        for playlist in res['items']:
            is_radio = 'radio' in playlist['name'].lower()
            progress_bar.update(1);

            if not is_radio:
                playlists.append(playlist['id'])

        offset += limit

    progress_bar.close()

    return playlists    


def get_songs_from_playlists(playlists):
    songs = []

    progress_bar = tqdm(total=len(playlists), desc="Filter Songs from Playlists", unit="track")   

    for playlist in playlists:
        progress_bar.update(1)

        uri = 'spotify:playlist:' + playlist
        res = sp.playlist_tracks(uri);

        for song in res['items']:
            songs.append(song['track']['id'])

    progress_bar.close()

    return songs


def extract_current_likes():
    limit = 20
    offset = 0
    tracks = []

    total_likes = None

    while True:
        res = sp.current_user_saved_tracks(limit=limit, offset=offset, market=None)

        if total_likes is None:
            total_likes = res['total']
            progress_bar = tqdm(total=total_likes, desc="Fetching Likes", unit="track")

        if not res['items']:
            break

        for item in res['items']:
            progress_bar.update(1)
            tracks.append(item['track']['id'])

        offset += limit

    progress_bar.close()

    return tracks


def dislike_songs(songs):
    if not songs:
        return
    
    progress_bar = tqdm(total=len(songs), desc="Disliking old songs", unit="track")
    
    for song in songs:
        progress_bar.update(1)
        sp.current_user_saved_tracks_delete(tracks=[song])

    progress_bar.close()


def like_songs(new_songs):
    if not new_songs:
        return
    
    progress_bar = tqdm(total=len(new_songs), desc="Liking new Songs", unit="track")

    for song in new_songs:
        progress_bar.update(1);
        sp.current_user_saved_tracks_add(tracks=[song])

    progress_bar.close()


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
        liked_songs = extract_current_likes()      
        dislike_songs(liked_songs)  
    
    playlists = get_user_playlists()
    new_songs = get_songs_from_playlists(playlists)

    like_songs(new_songs)

    print("Done ✅")
