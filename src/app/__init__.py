from flask import Flask

def create_app():
    app = Flask(__name__)

    from app.routes import mainbp
    from config import Config
    app.config.from_object(Config)
    app.register_blueprint(mainbp)
    return app



