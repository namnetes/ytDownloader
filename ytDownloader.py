#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import argparse
import re
from pytube import YouTube

def setup_logging():
    logging.basicConfig(
      filename='/var/log/ytdownloader.log',
      level=logging.INFO,
      format='%(asctime)s [%(levelname)s]: %(message)s'
    )

def process_file(input_file):
    with open(input_file, 'r') as file:
        for line in file:
            url = line.strip()
            process_url(url)

def process_url(url):
    if is_valid_url(url):
        print(f"URL valide : {url}")
    else:
        print(f"URL invalide : {url}")

def is_valid_url(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.scheme and parsed_url.netloc
    except ValueError:
        return False

def get_sorted_video_streams(yt):
    sq = yt.streams.filter(file_extension='mp4', only_video=True)
    return sq.order_by('resolution').asc()

def get_sorted_audio_streams(yt):
    sq = yt.streams.filter(file_extension='mp4', only_audio=True)
    return sq.order_by('bitrate').asc()

def get_highest_video_resolution(yt, user_resolution):
    sv = get_sorted_video_streams(yt)
    
    selected_stream = None
    for stream in sv:
        sres = int(re.search(r'\d+',stream.resolution).group())
        print(f"sres={sres}")
        if sres >= user_resolution: 
            selected_stream = stream
            break

    return selected_stream

def get_highest_audio_resolution(yt, user_bitrate):
    sa = get_sorted_audio_streams(yt)
    
    selected_stream = None
    for stream in sa:
        sbitrate = int(re.search(r'\d+', stream.abr).group())
        print(f"sbitrate={sbitrate}")
        if sbitrate >= user_bitrate: 
            selected_stream = stream
            break

    return selected_stream

def download_youtube_video():
    try:
        setup_logging()

        url = input("Entrez l'URL YouTube : ")
 
        yt = YouTube(url)
 
        title = yt.title
        resolution = yt.streams.get_highest_resolution().resolution
        print(f"resolution:{resolution}")
        filesize = yt.streams.get_highest_resolution().filesize
        # Demander à l'utilisateur d'entrer l'URL YouTube

        mimetype = yt.streams.get_highest_resolution().mime_type

        # Obtenir le flux de la résolution la plus élevée
        yd = yt.streams.get_highest_resolution()
        # Télécharger la vidéo dans le répertoire courant
        yd.download()

        # Enregistrement des informations dans le fichier de log
        log_message = f"Title: {title}; Resolution: {resolution}; Filesize: {filesize}; Mimetype: {mimetype}"
        logging.info(log_message)

        print("Téléchargement terminé.")
    except Exception as e:
        # Enregistrement des erreurs dans le fichier de log
        logging.error(f"Une erreur s'est produite : {str(e)}")

if __name__ == "__main__":
    """
    TODO: Ajoutez une description
    """
    
    # Mise en place de l'analyseur d'arguments en ligne de commande
    parser = argparse.ArgumentParser(
        description="YouTube video downloading tool.",
        epilog=('''The ytDownloader tool first separately downloads the
                video and audio streams before merging them with FFmpeg.
                  
                By default, the tool prioritizes the best available
                quality for both video and audio streams.
                  
                Please note that the -f/--input_file and URL options are
                mutually exclusive. Please use only one option at a time.
               ''')
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-f", "--input_file",
                        type=argparse.FileType('r'),
                        help="path to the file containing URLs to process.")
    group.add_argument("url",
                        nargs='?',
                        help="a YouTube video URL to download.")    

    parser.add_argument("-r", "--resolution",
                        type=int,
                        choices=['144', '240', '360', '480', '720', 
                                 '1080', '1440', '2160', '2880', '4320'],
                        help="desired video resolution.")
    parser.add_argument("-b", "--bitrate",
                        type=int,
                        choices=['128', '192', '256', '320'],
                        help="desired audio bitrate.")
    parser.add_argument("-d", "--dry-run",
                        action="store_true",
                        help="display information without downloading.")

    args = parser.parse_args()

    # si aucune résolution ou bitrate n'est fourni, les valeurs maximales
    # autorisées pour chacun des deux paramètres seront utilisées par défaut.
    if args.resolution is None:
        args.resolution = 4320

    if args.bitrate is None:
        args.bitrate = 320

    if args.input_file:
        print("L'option -f n'est pas encore disponible !")
        sys.exit(0)

    url = input("Entrez l'URL YouTube : ")
    yt = YouTube(url)

    sv = get_highest_video_resolution(yt, args.resolution)
    sa = get_highest_audio_resolution(yt, args.bitrate)
    if args.dry-run:
        print(f"{sv}\n{sa}")
    else:
        print("L'option de téléchargement n'est pas encore disponible !")

