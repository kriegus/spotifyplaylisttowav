import os
import spotipy
import spotipy.util as util
from youtube_search import YoutubeSearch
from pytube import YouTube

# Set up your credentials and create a Spotify object
client_id = 'enter here'
client_secret = 'enter here'
username = 'enter here'
scope = 'playlist-read-private'
redirect_uri = 'http://localhost:8888/callback' # replace with your registered redirect URI
token = util.prompt_for_user_token(username, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
if token:
    sp = spotipy.Spotify(auth=token)
    access_token = token
    print("Access token:", access_token)
else:
    print("Can't get token for", username)

# Set up the output directory
output_dir = "C:/Youtubemp3downloads"

# Get the playlist ID for your "FIFA" playlist
playlist_name = "enter here"
results = sp.current_user_playlists()
playlist_id = None
for item in results['items']:
    if item['name'] == playlist_name:
        playlist_id = item['id']
        break
if playlist_id is None:
    print(f"Playlist '{playlist_name}' not found")
else:
    print(f"Playlist ID for '{playlist_name}': {playlist_id}")
    print()

    # Download each song in the playlist
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")
    tracks = results['tracks']
    while tracks['next']:
        for item in tracks['items']:
            track = item['track']
            query = f"{track['artists'][0]['name']} {track['name']} lyrics"
            results = YoutubeSearch(query, max_results=1).to_dict()
            if results:
                url = f"https://www.youtube.com/watch?v={results[0]['id']}"
                yt = YouTube(url)
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=output_dir)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.wav'
                os.rename(out_file, new_file)
                print(f"{track['name']} by {track['artists'][0]['name']} has been successfully downloaded.")
            else:
                print(f"No results found for {query}")
        tracks = sp.next(tracks)
    for item in tracks['items']:
        track = item['track']
        query = f"{track['artists'][0]['name']} {track['name']} lyrics"
        results = YoutubeSearch(query, max_results=1).to_dict()
        if results:
            url = f"https://www.youtube.com/watch?v={results[0]['id']}"
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            out_file = video.download(output_path=output_dir)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.wav'
            os.rename(out_file, new_file)
            print(f"{track['name']} by {track['artists'][0]['name']} has been successfully downloaded.")
        else:
            print(f"No results found for {query}")
