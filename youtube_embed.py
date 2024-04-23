from googleapiclient.discovery import build

def get_youtube_trailer_url(game_name, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    search_response = youtube.search().list(
        q=f'{game_name} official trailer',
        part='snippet',
        maxResults=1,
        type='video'
    ).execute()

    if search_response['items']:
        video_id = search_response['items'][0]['id']['videoId']
        return f'https://www.youtube.com/embed/{video_id}'  # Use the embed URL format
    else:
        return None
