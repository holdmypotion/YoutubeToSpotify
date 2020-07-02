# TODO: Authorize with the YT client
# TODO: List 

import json
import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import requests
import youtube_dl

from spotify_client import SpotifyClient


class YoutubeClient:
    
    def __init__(self):
        self.youtube_client = self.get_youtube_client()
        self.tracks_info = {}
        self.spotify = SpotifyClient()
    
    def get_youtube_client(self):
        """
            Logs us into YouTube (copied)
        """
        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        api_service_name = "youtube"
        api_version = "v3"
        client_secrets_file = "./creds/client_secret_desktop.json"

        # Get credentials and create an API client
        scopes = ["https://www.googleapis.com/auth/youtube.readonly"]
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()

        # from the Youtube DATA API
        youtube_client = googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)

        return youtube_client
    
    def get_tracks_from_playlist(self):
        """
            Fetch all the videos from a particular playlist
        """
        request = self.youtube_client.playlistItems().list(
            part="snippet,contentDetails",
            maxResults=25,
            playlistId="PLcxNFMLUe0nKEn6kBOtiPxPbFedBPgbAn"
        )
        response = request.execute()
        # f = open('dict.json', 'w')
        # json_file = json.dumps(response)
        # f.write(json_file)
        # f.close()

        # print(response)

        # Looping through and picking up tracks
        for item in response['items']:
            video_title = item['snippet']['title']
            youtube_url = 'https://www.youtube.com/watch?v={}'.format(
                item['snippet']['resourceId']['videoId']
            )

            # Using youtube_dl to fetch track name and artist
            video = youtube_dl.YoutubeDL({'quiet': True}).extract_info(
            youtube_url, download=False
            )
            track = video['track']
            artist = video['artist']
            
            # Adding Needed info to the song_info dictionary
            if track is not None and artist is not None:
                self.tracks_info[video_title] = {
                    'youtube_url': youtube_url,
                    'track': track,
                    'artist': artist,
                    
                    # fetching the spotify uri for the track
                    'uri': self.spotify.search_song(artist, track),
                }
        
        return self.tracks_info
# https://www.youtube.com/watch?v=6ONRf7h3Mdk&list=PLcxNFMLUe0nKEn6kBOtiPxPbFedBPgbAn&index=2&t=0s
