from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

API_KEY = "be73c793a2bce7f8830ad7bc329aace9"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city')  
    if not city:
        return jsonify({"error": "City is required"}), 400
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={API_KEY}"
    try:
        response = requests.get(url)
        if response.status_code != 200:
            return jsonify({"error": "City not found or invalid API response"}), 404
        
        
        return jsonify(response.json())
    except requests.exceptions.RequestException as e:
       
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)