# YouTube Comment Subscription Bot

Ce projet contient un bot Python qui utilise l'API YouTube pour s'abonner aux commentateurs d'une vidéo spécifique.

## Configuration

Avant d'utiliser le bot, suivez ces étapes pour obtenir les informations nécessaires :

1. **Créer un projet dans la console Google Cloud :**
   - Accédez à [https://console.developers.google.com/](https://console.developers.google.com/).
   - Créez un nouveau projet ou sélectionnez un projet existant.

2. **Activer l'API YouTube :**
   - Dans le tableau de bord du projet, accédez à la section "Bibliothèque".
   - Recherchez "YouTube Data API v3" et activez-le pour votre projet.

3. **Configurer les identifiants OAuth :**
   - Toujours dans le tableau de bord du projet, accédez à la section "Identifiants".
   - Cliquez sur "Créer des identifiants" et choisissez "ID client OAuth".
   - Sélectionnez "Application de bureau" comme type d'application.
   - Téléchargez le fichier JSON contenant vos identifiants OAuth, renommez-le en `client-secrets.json`, et placez-le dans le répertoire du projet.

Votre fichier `client-secrets.json` doit ressembler à ceci :

```json
{
  "installed": {
    "client_id": "VOTRE_CLIENT_ID",
    "project_id": "VOTRE_PROJECT_ID",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_secret": "VOTRE_CLIENT_SECRET",
    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"]
  }
}
```


## Installation
Assurez-vous d'avoir Python installé sur votre machine.

Installez les dépendances en exécutant la commande suivante :
```bash
pip install -r requirements.txt
```


## Utilisation
Exécutez le script main.py pour démarrer le bot :

```bash
python main.py
```
Assurez-vous d'avoir remplacé la valeur de VIDEO_ID dans le fichier main.py par l'ID de la vidéo à laquelle vous souhaitez vous abonner.


## Fonctionnalités
add_subscription(youtube, channel_id): Ajoute un abonnement à la chaîne spécifiée.

get_comment_threads(youtube, video_id, max_results): Récupère les threads de commentaires pour une vidéo donnée.

subscribe_to_commenters(youtube, video_id, max_results=1): S'abonne aux utilisateurs ayant commenté une vidéo spécifique.

is_channel_subscribed(youtube, channelid_check): Vérifie si le bot est déjà abonné à une chaîne.

## Avertissement
Ce bot est fourni tel quel, sans garantie d'aucune sorte. Assurez-vous de respecter les conditions d'utilisation de l'API YouTube lors de son utilisation.
