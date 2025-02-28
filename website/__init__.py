from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
import os
from flask_migrate import Migrate
migrate = Migrate()

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)

    # app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    # app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your-secret-key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

    db.init_app(app)
    migrate.init_app(app, db)

    from .views import views
    from .pond_view import pond_view
    from .unit_view import unit_view
    from .job_view import job_view
    from .stock_view import stock_view
    from .auth import auth


    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(pond_view, url_prefix='/')
    app.register_blueprint(unit_view, url_prefix='/')
    app.register_blueprint(job_view, url_prefix='/')
    app.register_blueprint(stock_view, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Service_request, Monitoring_log, Units, Ponds, Stocktake, Soil_testing, Job_cards
    from werkzeug.middleware.proxy_fix import ProxyFix

    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

