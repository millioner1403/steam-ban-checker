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

@app.route('/get_bans', methods=['GET'])
def get_bans():
    # Получаем Steam ID из параметров запроса
    steam_id = request.args.get('steam_id')
    if not steam_id:
        return app.response_class(
            response=json.dumps({"error": "Steam ID is required"}, ensure_ascii=False),
            status=400,
            mimetype='application/json'
        )

    # Формируем запросы к Steam API
    bans_url = "https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/"
    summaries_url = "https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/"
    
    # Параметры для обоих запросов
    params = {"key": STEAM_API_KEY, "steamids": steam_id}

    try:
        # Отправляем запросы к Steam API
        bans_response = requests.get(bans_url, params=params)
        summaries_response = requests.get(summaries_url, params=params)

        # Проверяем, что оба запроса успешны
        if bans_response.status_code != 200 or summaries_response.status_code != 200:
            return app.response_class(
                response=json.dumps({"error": "Failed to fetch data from Steam API"}, ensure_ascii=False),
                status=500,
                mimetype='application/json'
            )

        # Извлекаем данные из ответов
        bans_data = bans_response.json().get("players", [{}])[0]
        summaries_data = summaries_response.json().get("response", {}).get("players", [{}])[0]

        # Формируем ответ с нужными данными в правильной последовательности
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

        return app.response_class(
            response=json.dumps(result, ensure_ascii=False),
            status=200,
            mimetype='application/json'
        )
    
    except Exception as e:
        return app.response_class(
            response=json.dumps({"error": str(e)}, ensure_ascii=False),
            status=500,
            mimetype='application/json'
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)