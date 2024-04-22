from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_youtube_trailer_url(game_name, api_key):
    try:
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', developerKey=api_key)
        request = youtube.search().list(
            q=f'{game_name} official trailer',
            part='snippet',
            maxResults=1,
            type='video'
        )
        response = request.execute()
        if response['items']:
            return f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
        else:
            return None
    except HttpError as e:
        if e.resp.status == 403:
            print("YouTube Data API quota exceeded. Please try again later.")
            return None
        else:
            raise
