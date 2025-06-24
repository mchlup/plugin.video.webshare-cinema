# -*- coding: utf-8 -*-
"""
Jednoduchý scraper na CSFD.cz pro Kodi plugin.
Vyhledává film/seriál podle názvu, vrací základní informace a plakát.
Nevyžaduje žádné speciální knihovny (jen requests a re).
"""
import requests
import re
from unidecode import unidecode

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Kodi plugin, https://github.com/mchlup/plugin.video.webshare-cinema)"
}

def csfd_search(title, mode='movie'):
    """
    Hledá film/seriál na CSFD.cz, vrací dict: title, year, rating, votes, poster, url
    """
    try:
        # Normalizace hledaného názvu
        search_term = unidecode(title)
        resp = requests.get(
            "https://www.csfd.cz/hledat/?q=" + requests.utils.quote(search_term),
            headers=HEADERS,
            timeout=5
        )
        if not resp.ok:
            return {}
        # Najdi první detail (odkaz na /film/ nebo /serial/)
        m = re.search(r'/([fs]erial|film)/(\d+)[^"]*"', resp.text)
        if not m:
            return {}
        detail_url = "https://www.csfd.cz" + m.group(0).strip('"')
        resp2 = requests.get(detail_url, headers=HEADERS, timeout=5)
        if not resp2.ok:
            return {}

        # Titulek
        m_title = re.search(r'<title>(.*?)\|', resp2.text)
        title_csfd = m_title.group(1).strip() if m_title else title

        # Rok
        m_year = re.search(r'(\d{4})', title_csfd)
        year = m_year.group(1) if m_year else ""

        # Hodnocení a počet hlasů
        m_rating = re.search(r'<h2.*?average.*?>([\d,]+)\s*%', resp2.text)
        rating = m_rating.group(1).replace(",", ".") if m_rating else ""
        m_votes = re.search(r'([0-9 ]+)\s*hodnocen[íi]', resp2.text)
        votes = m_votes.group(1).replace(" ", "") if m_votes else ""

        # Plakát
        m_poster = re.search(r'<img class="film-posters__img.*?src="([^"]+)"', resp2.text)
        poster = m_poster.group(1) if m_poster else ""

        # Popis
        m_desc = re.search(r'<div class="film-content__description.*?>(.*?)</div>', resp2.text, re.DOTALL)
        desc = re.sub('<.*?>', '', m_desc.group(1).strip()) if m_desc else ""

        return {
            "title": title_csfd,
            "year": year,
            "rating": rating,
            "votes": votes,
            "poster": poster,
            "desc": desc,
            "url": detail_url
        }
    except Exception as e:
        return {}
