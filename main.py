import os
import subprocess
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Remplacez ces valeurs par les vôtres
CLIENT_SECRETS_FILE = "client-secrets.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = build(API_NAME, API_VERSION, credentials=credentials)
    return youtube


def add_subscription(youtube, channel_id):
    request = youtube.subscriptions().insert(
        part="snippet",
        body={
            "snippet": {
                "resourceId": {
                    "channelId": channel_id
                }
            }
        }
    )

    try:
        response = request.execute()
        print("Abonnement réussi.")
    except Exception as e:
        print(f"Erreur lors de l'abonnement : {str(e)}")

def get_video_comments(youtube, video_id, max_results=100):
    comments = []

    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        order="relevance",
        textFormat="plainText",
        maxResults=max_results
    )

    while request:
        response = request.execute()
        for item in response["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
            comments.append(comment)

        request = youtube.commentThreads().list_next(request, response)

    return comments


def subscribe_to_commenters(youtube, video_id, max_results=100):
    print("Récupération des commenteurs")
    commenters = get_video_comments(youtube, video_id, max_results)

    for commenter_id in commenters:
        add_subscription(youtube, commenter_id)
        print(f"Abonnement à la chaîne {commenter_id} effectué.")

if __name__ == '__main__':
    youtube_service = get_authenticated_service()

    # Remplacez VIDEO_ID par l'ID de la vidéo dont vous souhaitez récupérer les commentaires
    VIDEO_ID = "tnTPaLOaHz8"

    subscribe_to_commenters(youtube_service, VIDEO_ID)

