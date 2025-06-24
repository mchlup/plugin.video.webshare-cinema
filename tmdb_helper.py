import requests
import xbmcgui
import xbmc
import os

class TMDbHelper:
    def __init__(self, addon):
        self.addon = addon
        self.API_TOKEN = addon.getSetting('tmdb_token')
        self.LANG = addon.getSetting('tmdb_lang') or 'cs-CZ'
        self.BASE_URL = "https://api.themoviedb.org/3"
        
    def search_movie(self, title):
        url = f"{self.BASE_URL}/search/movie"
        params = {
            "api_key": self.API_TOKEN,
            "query": title,
            "language": self.LANG,
            "include_adult": "false"
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            return data.get("results", [])
        return []

    def get_movie_details(self, movie_id):
        url = f"{self.BASE_URL}/movie/{movie_id}"
        params = {
            "api_key": self.API_TOKEN,
            "language": self.LANG
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json()
        return None

    def enrich_listitem(self, listitem, metadata):
        if not metadata:
            return listitem
            
        # Add title and original title
        title = metadata.get('title', '')
        original_title = metadata.get('original_title', '')
        listitem.setLabel(title)
        
        # Add poster
        if metadata.get('poster_path'):
            poster_url = f"https://image.tmdb.org/t/p/w500{metadata['poster_path']}"
            listitem.setArt({'poster': poster_url, 'thumb': poster_url})
            
        # Add plot and year
        info = {
            'title': title,
            'originaltitle': original_title,
            'plot': metadata.get('overview', ''),
            'year': metadata.get('release_date', '')[:4] if metadata.get('release_date') else None
        }
        listitem.setInfo('video', info)
        
        return listitem
