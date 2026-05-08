from flask import Flask
from config import Config
from models import db
from routes.ugc import ugc_bp


def create_app():
    app = Flask(__name__)
    
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(ugc_bp)
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)