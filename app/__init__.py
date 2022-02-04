import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config
from flask_swagger_ui import get_swaggerui_blueprint


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    with app.app_context():
        db.create_all()

    from app.api import bp as api_bp
    app.register_blueprint(api_bp,url_prefix='/api')

    swagger_url = '/swagger'
    api_url = '/static/swagger.json'
    swagger_blueprint = get_swaggerui_blueprint(swagger_url,api_url,config={'app_name':"Gira"})
    app.register_blueprint(swagger_blueprint, url_prefix=swagger_url)

    return app
