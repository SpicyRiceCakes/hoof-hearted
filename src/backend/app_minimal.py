#!/usr/bin/env python3
"""Minimal test version to identify the hanging issue"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

print("🐎 Starting minimal Hoof Hearted Backend...")

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-in-production')
CORS(app, origins="*")

@app.route('/health')
def health_check():
    return jsonify({'status': 'healthy', 'service': 'minimal-backend'})

@app.route('/api/health')
def api_health_check():
    return jsonify({'status': 'healthy', 'service': 'minimal-backend'})

@app.route('/api/status')
def api_status():
    return jsonify({
        'api_version': '1.0.0',
        'status': 'operational',
        'message': 'Minimal backend working!',
        'korean_fart_humor': '공구공구 (gong-goo-gong-goo)'
    })

if __name__ == '__main__':
    print(f"🚀 Starting minimal Flask on 0.0.0.0:5000")
    app.run(host='0.0.0.0', port=5000, debug=False)