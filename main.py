# from datetime import datetime
from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint

# date_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD\n")
# date = datetime.strptime(date_input, "%Y-%m-%d")
# print(date)

date_input = "2021-12-25"

URL = f"https://www.billboard.com/charts/hot-100/{date_input}/"

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
song = soup.find_all(name="h3", class_="u-max-width-230@tablet-only")
song_names = [_.getText().strip() for _ in song]
# print(title)
artist = soup.find_all(name="span", class_="u-max-width-230@tablet-only")
artist_list = [_.getText().strip() for _ in artist]
# print(artist_list)

Client_ID = "f926df69460144f9bdbdca0eeb37f38c"
Client_Secret = "b2738bf42d5f4733b16b380e166f0aba"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                                               redirect_uri="http://example.com",
                                               client_id=Client_ID,
                                               client_secret=Client_Secret,
                                               show_dialog=True,
                                               cache_path="token.txt"))
user_id = sp.current_user()["id"]
# print(user_id)

song_uris = []
for i in range(0, len(song_names)):
    result = sp.search(q=f"track:{song_names[i]} artist:{artist_list[i]}", type="track")
    # print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# print(song_uris)


playlist = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100", public=False)
print(playlist)

sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)