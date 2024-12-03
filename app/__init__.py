from flask import Flask

def create_app():
    app = Flask(__name__)
    from .decrypt_server import decrypt_bp
    app.register_blueprint(decrypt_bp)
    return app
