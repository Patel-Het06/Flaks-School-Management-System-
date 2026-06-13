from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config
from models import User
from extensions import db, mail, login_manager


def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)         
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view= 'auth.login'


    @login_manager.user_loader
    def load_user(user_id):
        print("Loading user:", user_id)  # ← add this
        return db.session.get(User , int(user_id))

    from routes.auth import auth
    from routes.user import user
    from routes.admin import admin

    app.register_blueprint(auth)
    app.register_blueprint(user)
    app.register_blueprint(admin)

    return app
app=create_app()

if __name__=='__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
