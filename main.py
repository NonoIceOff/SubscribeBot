from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from colorama import Fore, Style

# Remplacez ces valeurs par les vôtres
CLIENT_SECRETS_FILE = "client-secrets.json"
API_NAME = "youtube"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def get_authenticated_service():
    try:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        youtube = build(API_NAME, API_VERSION, credentials=credentials)
        return youtube
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'initialisation du service YouTube : {str(e)}" + Style.RESET_ALL)
        return None


def add_subscription(youtube, channel_id):
    try:
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
        response = request.execute()
        print(Fore.GREEN + "Abonnement réussi." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Erreur lors de l'abonnement : {str(e)}" + Style.RESET_ALL)


def comment_on_video(youtube, video_id, comment_text):
    try:
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
                "snippet": {
                    "topLevelComment": {
                        "snippet": {
                            "videoId": video_id,
                            "textOriginal": comment_text
                        }
                    }
                }
            }
        )
        response = request.execute()
        print(Fore.GREEN + "Commentaire réussi." + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"Erreur lors du commentaire : {str(e)}" + Style.RESET_ALL)


def subscribe_to_commenters(youtube, video_id, max_results=1):
    try:
        commenters = get_comment_threads(youtube, video_id, max_results)
        print(Fore.CYAN + "Récupération des commentateurs réussie !" + Style.RESET_ALL)

        for commenter_id in commenters:
            id_guy = commenter_id["snippet"]["topLevelComment"]["snippet"]["authorChannelId"]["value"]
            print(Fore.YELLOW + f"ChaîneID {id_guy} récupérée" + Style.RESET_ALL)

            if not is_channel_subscribed(youtube, id_guy):
                add_subscription(youtube, id_guy)
                print(Fore.GREEN + f"Abonnement à la chaîne {id_guy} effectué." + Style.RESET_ALL)

                # Commenter la première vidéo du commentateur
                first_video_id = get_first_video_id(youtube, id_guy)
                if first_video_id:
                    comment_text = "Je suis totalement apagnan de ta vidéo, je m'abonne !"
                    comment_on_video(youtube, first_video_id, comment_text)

                print("------------")
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la récupération des commentateurs : {str(e)}" + Style.RESET_ALL)


def is_channel_subscribed(youtube, channelid_check):
    try:
        subscriptions_response = youtube.subscriptions().list(
            part='snippet',
            mine=True,
            order='alphabetical'
        ).execute()

        for item in subscriptions_response.get("items", []):
            if channelid_check == item["snippet"]["resourceId"]["channelId"]:
                return True
        return False
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la vérification de l'abonnement : {str(e)}" + Style.RESET_ALL)
        return False


def get_comment_threads(youtube, video_id, max_results):
    try:
        results = youtube.commentThreads().list(
            part="snippet",
            maxResults=max_results,
            videoId=video_id,
            textFormat="plainText"
        ).execute()

        return results.get("items", [])
    except Exception as e:
        print(Fore.RED + f"Erreur lors de la récupération des commentaires : {str(e)}" + Style.RESET_ALL)
        return []


def get_first_video_id(youtube, channel_id):
    try:
        uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)
        if uploads_playlist_id:
            playlist_items = youtube.playlistItems().list(
                part="contentDetails",
                playlistId=uploads_playlist_id,
                maxResults=1
            ).execute()

            items = playlist_items.get("items", [])
            if items:
                return items[0]["contentDetails"]["videoId"]
            else:
                print(Fore.YELLOW + "Aucune vidéo trouvée dans la playlist d'uploads." + Style.RESET_ALL)
                return None
        else:
            print(Fore.YELLOW + "Aucune playlist d'uploads trouvée pour la chaîne spécifiée." + Style.RESET_ALL)
            return None
    except Exception as e:
        if e.resp.status == 404:
            print(Fore.YELLOW + "Playlist d'uploads non trouvée. Le gars n'a peut-être pas de vidéo." + Style.RESET_ALL)
            return None
        else:
            print(Fore.RED + f"Erreur lors de la récupération de la première vidéo : {str(e)}" + Style.RESET_ALL)
            return None
    except Exception as e:
        print(Fore.RED + f"Erreur inattendue lors de la récupération de la première vidéo : {str(e)}" + Style.RESET_ALL)
        return None




def get_uploads_playlist_id(youtube, channel_id):
    try:
        channels_response = youtube.channels().list(
            part="contentDetails",
            id=channel_id
        ).execute()

        items = channels_response.get("items", [])
        if items:
            return items[0]["contentDetails"]["relatedPlaylists"]["uploads"]
    except Exception as e:
        print(
            Fore.RED + f"Erreur lors de la récupération de l'ID de la playlist d'uploads : {str(e)}" + Style.RESET_ALL)

    return None


if __name__ == '__main__':
    print(Fore.MAGENTA + "Initialisation du service YouTube..." + Style.RESET_ALL)
    youtube_service = get_authenticated_service()

    if youtube_service:
        VIDEO_ID = "Dg9yrA-18y4"
        print(Fore.MAGENTA + f"Abonnement aux commentateurs de la vidéo {VIDEO_ID}..." + Style.RESET_ALL)
        subscribe_to_commenters(youtube_service, VIDEO_ID, 200)
