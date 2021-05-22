import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import dotenv
import os



date = input("Which year you want to travel? enter the date in this format YYYY-MM-DD : ")



response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
data=response.text
soup = BeautifulSoup(data,"html.parser")
soup.prettify()
names = soup.find_all(name="span",class_="chart-element__information__song text--truncate color--primary")
songs=[]

for name in names:
    songs.append(name.string)

# print(songs)



dotenv.load_dotenv("E:\\Env Variables\\my_env.env")
SPOTIPY_CLIENT_ID = os.getenv("spotify_Client_ID")
SPOTIPY_CLIENT_SECRET=os.getenv("spotify_Client_Secret")
OAUTH_AUTHORIZE_URL= 'https://accounts.spotify.com/authorize'
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'



sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                               client_secret=SPOTIPY_CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               show_dialog=True,
                                               cache_path="token.txt"
                                               ))

user_id = sp.current_user()["id"]

year=date.split('-')[0]
songs_uris=[]

for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        songs_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(songs_uris)

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
# print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=songs_uris)

