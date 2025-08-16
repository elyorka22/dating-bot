from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running! Status: OK"

@app.route('/health')
def health():
    return "OK"

@app.route('/status')
def status():
    return "Bot is running!"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    print(f"Starting Flask app on port {port}")
    app.run(host='0.0.0.0', port=port) 