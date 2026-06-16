from flask import Flask, request, jsonify, send_from_directory
import os, requests as req

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

@app.route('/')
def index():
    return send_from_directory(STATIC_DIR, 'po-router.html')

@app.route('/api/anthropic', methods=['POST', 'OPTIONS'])
def proxy():
    if request.method == 'OPTIONS':
        r = jsonify({'ok': True})
        r.headers['Access-Control-Allow-Origin'] = '*'
        r.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return r
    d = request.json.copy()
    k = d.pop('_apiKey', None) or os.environ.get('ANTHROPIC_API_KEY', '')
    try:
        r = req.post('https://api.anthropic.com/v1/messages', headers={'Content-Type':'application/json','x-api-key':k,'anthropic-version':'2023-06-01'}, json=d, timeout=120)
        return jsonify(r.json()), r.status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 5001)))
