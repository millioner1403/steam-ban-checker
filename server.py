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

    # Формируем запрос к Steam API
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/"
    params = {
        "key": STEAM_API_KEY,
        "steamids": steam_id
    }

    # Отправляем запрос и возвращаем результат
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to fetch data from Steam API"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)