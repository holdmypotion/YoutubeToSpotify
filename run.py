from spotify_client import SpotifyClient
from youtube_client import YoutubeClient

def run():
    """
        Exceutes the whole program
    """
    # Authenticate with youtube and spotify
    youtube = YoutubeClient()
    spotify = SpotifyClient()

    # Get all the songs from the tracks playlist on YT
    all_em_tracks = youtube.get_tracks_from_playlist()

    # Add em
    spotify.add_songs(all_em_tracks)

if __name__ == '__main__':
    run()
