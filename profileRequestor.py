import requests
import json

with open('auth.json') as f:
    HyKey = json.load(f)['hypixelApiKey']


def get_profile(player_username, profile_name):
    data = requests.get("https://api.hypixel.net/player?key="+HyKey+"&name="+player_username).json()
    profileID = 0
    found = 0
    for key in data['player']['stats']['SkyBlock']['profiles']:
        if data['player']['stats']['SkyBlock']['profiles'][key]['cute_name'] == profile_name:
            profileID = data['player']['stats']['SkyBlock']['profiles'][key]['profile_id']
            found = 1
    profile = requests.get("https://api.hypixel.net/Skyblock/profile?key="+HyKey+"&profile="+profileID).json()
    if found:
        return profile['profile']['members'][profileID]
    else:
        return -1
