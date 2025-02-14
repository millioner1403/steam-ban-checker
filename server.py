from flask import Flask, request
import requests
import os
import json
from collections import OrderedDict
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Получаем API ключ из переменных окружения
STEAM_API_KEY = os.getenv("STEAM_API_KEY")
print(f"STEAM_API_KEY: {STEAM_API_KEY}")  # Логируем, загружается ли ключ

@app.route('/')
def home():
    return "Steam Ban Checker API is running!", 200

@app.route('/get_bans', methods=['GET'])
def get_bans():
    steam_id = request.args.get('steam_id')
    if not steam_id:
        return {"error": "Steam ID is required"}, 400

    bans_url = "https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/"
    summaries_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    
    params = {"key": STEAM_API_KEY, "steamids": steam_id}
    print(f"Requesting Steam API with: {params}")  # Лог запроса

    try:
        bans_response = requests.get(bans_url, params=params)
        summaries_response = requests.get(summaries_url, params=params)

        if bans_response.status_code != 200 or summaries_response.status_code != 200:
            return {"error": "Failed to fetch data from Steam API"}, 500

        bans_data = bans_response.json().get("players", [{}])[0]
        summaries_data = summaries_response.json().get("response", {}).get("players", [{}])[0]

        result = OrderedDict([
            ("avatarfull", summaries_data.get("avatarfull")),
            ("personaname", summaries_data.get("personaname")),
            ("SteamId", summaries_data.get("steamid")),
            ("profileurl", summaries_data.get("profileurl")),
            ("VACBanned", bans_data.get("VACBanned")),
            ("NumberOfVACBans", bans_data.get("NumberOfVACBans")),
            ("NumberOfGameBans", bans_data.get("NumberOfGameBans")),
            ("CommunityBanned", bans_data.get("CommunityBanned")),
            ("EconomyBan", bans_data.get("EconomyBan")),
            ("DaysSinceLastBan", bans_data.get("DaysSinceLastBan"))
        ])

        return json.dumps(result, ensure_ascii=False), 200
    
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Railway сам задает порт
    app.run(host='0.0.0.0', port=port)