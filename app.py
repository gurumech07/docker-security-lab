from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "Docker Security Lab: Application Running Safely!"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

if __name__ == '__main__':
    # For development only
    app.run(host='0.0.0.0', port=5000)
