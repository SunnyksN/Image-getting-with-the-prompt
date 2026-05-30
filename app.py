import os
import requests
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from urllib.parse import quote


load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = request.get_json()

    prompt = data.get('prompt', '').strip()

    if not prompt:
        return jsonify({
            'error': 'Please enter a description.'
        }), 400

    url = "https://api.unsplash.com/photos/random"

    headers = {
        "Authorization":
        f"Client-ID {UNSPLASH_ACCESS_KEY}"
    }

    params = {
        "query": prompt,
        "orientation": "landscape"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params
        )

        print(response.status_code)
        print(response.text)

        if response.status_code != 200:
            return jsonify({
                'error':
                f"Unsplash API Error: "
                f"{response.status_code}"
            }), 500

        image_data = response.json()

        image_url = image_data["urls"]["regular"]

        return jsonify({
            'image_url': image_url,
            'prompt': prompt
        })

    except Exception as e:
        print(e)

        return jsonify({
            'error': str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)