import requests 
import urllib.parse

from flask import Flask, redirect, request, jsonify, session
from datetime import datetime, timedelta

def filterSongsByDuration(song_database: List[dict], min_duration: float, max_duration: float):
    '''
        Inputs:
        - song_database: List[dict] specifies that song_database is a list of dictionaries 
        (assuming each song is represented as a dictionary with details like title, artist, and duration).
        - min_duration and max_duration is the range in which the playlist can fall in. e.g. a playlist is 15 minutes 
        we might want the playlist to fall between 14 1/2 to 15 1/2 minutes

    '''

    
    return