from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import sqlalchemy as sa

db = SQLAlchemy()
db_info = {
    'username': 'root',
    'password': '1',
    'host': 'localhost',
    'database': 'demo'
}

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'some secret string'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_info['username']}:{db_info['password']}@{db_info['host']}/{db_info['database']}"
    
    from .views import viewsBP
    from .auth import authBP

    app.register_blueprint(viewsBP)
    app.register_blueprint(authBP)

    db.init_app(app=app) # initialize the app with the sqlalchemy extension

    from .models import User, Record

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'authBP.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return db.session.get(User, int(id))

    return app
