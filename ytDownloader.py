#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
from datetime import datetime
from pytube import YouTube

def setup_logging():
    logging.basicConfig(
      filename='/var/log/ytdownloader.log',
      level=logging.INFO,
      format='%(asctime)s [%(levelname)s]: %(message)s'
    )


def download_youtube_video():
    try:
        setup_logging()

        # Demander à l'utilisateur d'entrer l'URL YouTube
        url = input("Entrez l'URL YouTube : ")
 
        yt = YouTube(url)
 
        title = yt.title
        resolution = yt.streams.get_highest_resolution().resolution
        filesize = yt.streams.get_highest_resolution().filesize
        mimetype = yt.streams.get_highest_resolution().mime_type

        # Obtenir le flux de la résolution la plus élevée
        yd = yt.streams.get_highest_resolution()
 
        # Télécharger la vidéo dans le répertoire courant
        yd.download()

        # Enregistrement des informations dans le fichier de log
        log_message = f"Title: {title}, Resolution: {resolution}, Filesize: {filesize}, Mimetype: {mimetype}"
        logging.info(log_message)

        print("Téléchargement terminé.")
    except Exception as e:
        # Enregistrement des erreurs dans le fichier de log
        logging.error(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    # Appeler la fonction principale si le script est exécuté en tant que programme principal
    download_youtube_video()
