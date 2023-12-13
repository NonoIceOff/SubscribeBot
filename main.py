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
    commenters = get_comment_threads(youtube, video_id,max_results)
    print("Récupération des commenteurs réussi !")

    for commenter_id in commenters:
        id_guy = commenter_id["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
        print(f"ChaîneID {id_guy} récupérée")
        if is_channel_subscribed(youtube) == False:
            add_subscription(youtube, id_guy)
            print(f"Abonnement à la chaîne {commenter_id['snippet']['authorDisplayName']} effectué.")
            print("------------")

def is_channel_subscribed(youtube):
    subscriptions_response = youtube.subscriptions().list(
        part='snippet',
        mine=True,
        maxResults=50,
        order='alphabetical').execute()
    print(subscriptions_response)
    return False

if __name__ == '__main__':
    youtube_service = get_authenticated_service()
    VIDEO_ID = "tnTPaLOaHz8"
    #is_channel_subscribed(youtube_service)
    subscribe_to_commenters(youtube_service, VIDEO_ID)
