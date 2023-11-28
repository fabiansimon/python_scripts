import spotipy
from spotipy.oauth2 import SpotifyOAuth

client_id = 'e4b7995e48d14b2ca810a1f79c0dabc9'
client_secret = '4112d697ba5f45b280f090bd5144a2df'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, redirect_uri='http://localhost:8888/callback', scope='playlist-read-private'))


def search_track(query):
    # Search for a track
    results = sp.search(q=query, type='track', limit=1)

    # Print some information about the track
    if results['tracks']['items']:
        track = results['tracks']['items'][0]
        print(f"Track: {track['name']}")
        print(f"Artist(s): {', '.join([artist['name'] for artist in track['artists']])}")
        print(f"Album: {track['album']['name']}")
        print(f"Preview URL: {track['preview_url']}")
    else:
        print(f"No results found for '{query}'")

def get_user_playlists():
    res = sp.current_user_playlists(limit=50, offset=0);
    playlists = []

    for playlist in res['items']:
        is_radio = playlist['name'].lower().find("radio") != -1
        print(f"Playlist: {playlist['name']}" + f"; is radio: {is_radio}")
        if not is_radio:
            playlists.append(playlist['id'])

    for item in playlists:
        print(item)

    

if __name__ == "__main__":
    # Example usage: search for a track by name
    # track_name = input("Enter a track name: ")
    # search_track(track_name)
    get_user_playlists()
