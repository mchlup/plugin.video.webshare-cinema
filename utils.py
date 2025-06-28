import re

EPISODE_PATTERNS = [
    r'[sS](\d+)[eE](\d+)',  # S01E01, s01e01
    r'[sS](\d+)\s*[eE](\d+)',  # S01 E01
    r'(\d+)x(\d+)',  # 1x01
]

def is_episode(filename):
    for pattern in EPISODE_PATTERNS:
        if re.search(pattern, filename):
            return True
    return False

def get_episode_info(filename):
    for pattern in EPISODE_PATTERNS:
        match = re.search(pattern, filename)
        if match:
            return {
                'season': int(match.group(1)),
                'episode': int(match.group(2))
            }
    return None


import xbmcaddon

def save_token_info(token, expiry):
    addon = xbmcaddon.Addon()
    addon.setSetting("webshare_token", token)
    addon.setSetting("webshare_token_expiry", expiry)
