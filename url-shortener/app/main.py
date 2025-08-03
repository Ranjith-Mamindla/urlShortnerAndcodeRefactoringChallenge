from flask import Flask, Blueprint, request, jsonify, redirect, abort
from app.models import url_store
from app.utils import generate_short_code, is_valid_url
from threading import Lock
from datetime import datetime

main_bp = Blueprint('main', __name__)
lock = Lock()

@main_bp.route('/')
def health_check():
    return jsonify({"service":"URL Shortener API", "status":"healthy"})

@main_bp.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing 'url' field"}), 400

    long_url = data['url'].strip()
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    with lock:
        # Prevent duplicates: check if URL is already shortened
        for code, info in url_store.items():
            if info['url'] == long_url:
                short_code = code
                break
        else:
            # Generate unique short code
            short_code = generate_short_code()
            while short_code in url_store:
                short_code = generate_short_code()
            url_store[short_code] = {
                "url": long_url,
                "created_at": datetime.utcnow(),
                "clicks": 0
            }

    short_url = request.host_url + short_code
    return jsonify({"short_code": short_code, "short_url": short_url})

@main_bp.route('/<short_code>', methods=['GET'])
def redirect_url(short_code):
    with lock:
        if short_code not in url_store:
            abort(404, description="Short code not found")
        url_store[short_code]['clicks'] += 1
        original_url = url_store[short_code]['url']

    return redirect(original_url)

@main_bp.route('/api/stats/<short_code>', methods=['GET'])
def stats(short_code):
    with lock:
        if short_code not in url_store:
            return jsonify({"error": "Short code not found"}), 404
        info = url_store[short_code]
        return jsonify({
            "url": info['url'],
            "clicks": info['clicks'],
            "created_at": info['created_at'].isoformat() + "Z"
        })

def create_app():
    app = Flask(__name__)
    app.register_blueprint(main_bp)
    return app

# For flask CLI usage: python -m flask --app app.main run
app = create_app()
