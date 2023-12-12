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

if __name__ == '__main__':
    youtube_service = get_authenticated_service()

    # Remplacez CHANNEL_ID par l'ID de la chaîne à laquelle vous souhaitez vous abonner
    CHANNEL_ID = "UCo33niDKpTpgwZ_dohqvylg"

    add_subscription(youtube_service, CHANNEL_ID)
