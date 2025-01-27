from flask import Flask, request, jsonify
import requests
import os  # Для работы с переменными окружения

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
        return jsonify({"error": "Steam ID is required"}), 400

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
            return jsonify({"error": "Failed to fetch data from Steam API"}), 500

        # Извлекаем данные из ответов
        bans_data = bans_response.json().get("players", [{}])[0]
        summaries_data = summaries_response.json().get("response", {}).get("players", [{}])[0]

        # Формируем ответ в нужной последовательности
        result = {
            "Avatar": summaries_data.get("avatarfull"),
            "Name": summaries_data.get("personaname"),
            "Link to Profile": summaries_data.get("profileurl"),
            "SteamID": steam_id,
            "VAC Bans": bans_data.get("VACBanned"),
            "Number Of VAC Bans": bans_data.get("NumberOfVACBans"),
            "Number Of Game Bans": bans_data.get("NumberOfGameBans", 0),  # Может отсутствовать
            "Days Since Last Ban": bans_data.get("DaysSinceLastBan"),
            "Community Banned": bans_data.get("CommunityBanned"),
            "Economy Ban": bans_data.get("EconomyBan"),
        }

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)