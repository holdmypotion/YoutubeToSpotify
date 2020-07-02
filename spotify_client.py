import os
import json
import urllib
import requests

from creds import secrets
from exceptions import ResponseException

SPOTIFY_ID = secrets.SPOTIFY_ID
SPOTIFY_TOKEN = secrets.SPOTIFY_TOKEN

class SpotifyClient():
    """
        Manage all the interaction with the Spotify API
    """

    def create_playlist(self):
        """ Creates a new playlist"""
        request_body = json.dumps({
            'name': 'YouTube Liked',
            'description': 'Liked songs from YT',
            'public': False
        })

        # Post request
        url = f'https://api.spotify.com/v1/users/{SPOTIFY_ID}/playlists'
        res = requests.post(
            url,
            data=request_body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {SPOTIFY_TOKEN}'
            }
        )
        res_json = res.json()
        result = res_json

        # Playlist ID
        print('Created a new playlist\n')
        return res_json['id']

    def fetch_playlist(self, name):
        """
            Fetches a particular playlist
        """
        url = f'https://api.spotify.com/v1/users/{SPOTIFY_ID}/playlists'
        res = requests.get(
            url,
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {SPOTIFY_TOKEN}'
            }
        )

        res_json = res.json()
        playlists = res_json['items']

        # Looping through the list of playlists to find
        # the particular playlist based on the name
        for playlist in playlists:
            if playlist['name'] == name:
                print('Playlist Fetched\n')
                return playlist['owner']['id']

    def search_song(self, artist, track):
        """
            Search for the songs based on artist and track
        """
        url = f'https://api.spotify.com/v1/search?query=track%3A{track}+artist%3a{artist}&type=track'
        res = requests.get(
            url,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {SPOTIFY_TOKEN}'
            }
        )
        res_json = res.json()
        f = open('dict.json', 'w')
        json_file = json.dumps(res_json)
        f.write(json_file)
        f.close()

        songs = res_json['tracks']['items']
        if songs:
            # Take the first fetched result
            print('Got the song\n')
            return songs[0]['uri']
            
        else: 
            raise Exception(f'No songs were found for {artist} = {track}')

    def add_songs(self, tracks_info):
        """
            Add songs to the above created playlist
        """
        # Getting details about the tracks available in the playlist
        # tracks_info = YoutubeClient.get_tracks_from_playlist()

        # Fetching all the spotify uris as list
        uris = [track_info['uri'] for track_info in tracks_info.values()]
        request_body = json.dumps(uris)

        # Creating / Fetching the playlist
        playlist_id = self.fetch_playlist('YouTube Liked')
        if not playlist_id:
            playlist_id = self.create_playlist()

        url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
        res = requests.post(
            url,
            data=request_body,
            headers={
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {SPOTIFY_TOKEN}'
            }
        )

        if res.status_code != 201:
            raise ResponseException(res.status_code)
        else:
            print('Songs Added Bruh!!!')
            
        res_json = res.json()
        return res_json


# Driver
if __name__ == '__main__':

#     obj = SpotifyClient()



#     # Seaching the song
#     # song_uri = str(obj.search_song('Travis Scott', 'SICKO MODE'))
#     # song_uri = obj.search_song('Roddy Ricch', 'The Box')
#     obj.songs_info = {
#         {
#             'artist': 'Travis Scott',
#             'track': 'SICKO MODE',
#             'uri': str(obj.search_song('Travis Scott', 'SICKO MODE')),
#         },
#         {   
#             'artist': 'Roddy Ricch',
#             'track': 'The Box',
#             'uri': str(obj.search_song('Roddy Ricch', 'The Box')),
#         },
#     }

#     # Adding the song
#     obj.add_songs(playlist_id)
    obj = SpotifyClient()

    print(obj.search_song('Polo G', 'Be Something'))