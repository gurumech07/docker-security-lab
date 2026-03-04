from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def hello():
    return "Docker Security Lab: Application Running Safely!"

@app.route('/health')
def health():
    return jsonify({"status": "healthy"}), 200

@app.after_request
def add_security_headers(response):
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    # For development only
    app.run(host='0.0.0.0', port=5000)
