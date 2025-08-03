from flask import Flask
from routes.user_routes import user_bp

app = Flask(__name__)
app.register_blueprint(user_bp)

@app.route('/')
def home():
    return "User Management System"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
