from flask import Flask, request, jsonify
import requests
import os
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
        bans_data = bans_response.json()
        summaries_data = summaries_response.json()

        # Возвращаем данные без изменений
        return jsonify({
            "bans_data": bans_data,
            "summaries_data": summaries_data
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000
