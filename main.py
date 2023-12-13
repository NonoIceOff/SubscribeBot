from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Remplacez ces valeurs par les vôtres
CLIENT_SECRETS_FILE = "client-secrets.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]



def reply_to_comment(youtube, video_id, parent_id, text ):
    request = youtube.comments().insert(
        part="snippet",
        body={
            "snippet": {
                "parentId": parent_id,
                "textOriginal": text
            }
        }
    )
    try:
        response = request.execute()
        print(f"Réponse au commentaire réussie : {text}")
    except Exception as e:
        print(f"Erreur lors de la réponse au commentaire : {str(e)}")


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

def get_comment_threads(youtube, video_id, max_results):
    results = youtube.commentThreads().list(
    part="snippet",
    maxResults=max_results,
    videoId=video_id,
    textFormat="plainText"
    ).execute()
    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        author = comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
    return results["items"]

def subscribe_to_commenters(youtube, video_id, max_results=5):
    commenters = get_comment_threads(youtube, video_id, max_results)
    print("Récupération des commentateurs réussie !")

    for commenter in commenters:
        id_guy = commenter["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
        comment_id = commenter["id"]
        print(f"ChaîneID {id_guy} récupérée")

        if not is_channel_subscribed(youtube, id_guy):
            add_subscription(youtube, id_guy)
            print(f"Abonnement à la chaîne {id_guy}")

            # Ajouter une réponse au commentaire
            reply_text = "Je suis vraiment Apagnan de votre chaine youtube !"
            reply_to_comment(youtube, video_id, comment_id, reply_text)


def is_channel_subscribed(youtube, channelid_check):
    subscriptions_response = youtube.subscriptions().list(
        part='snippet',
        mine=True,
        maxResults=50,
        order='alphabetical').execute()
    print(subscriptions_response)
    for item in subscriptions_response["items"]:
        if channelid_check == item["snippet"]["resourceId"]["channelId"]:
            return True
    return False

if __name__ == '__main__':
    youtube_service = get_authenticated_service()
    VIDEO_ID = "tnTPaLOaHz8"
    #is_channel_subscribed(youtube_service)
    subscribe_to_commenters(youtube_service, VIDEO_ID)
