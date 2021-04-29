import os

from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, current_user

from app.blueprints.user.routes import user
from app.database.base import session
from app.models.Model import Vendedores






def create_app():
    app = Flask(__name__, static_folder='static')
    app.secret_key = os.urandom(24)



    login_manager = LoginManager()
    login_manager.login_view = 'user.login'
    login_manager.init_app(app)


    @app.errorhandler(404)
    @app.route('/<pagename>')
    def admin(pagename):
        result = render_template('page-404.html', title='Error')
        return result


    @login_manager.user_loader
    def load_user(seller_id):
        return session.query(Vendedores).get(int(seller_id))


    @app.route('/')
    def home():
        if current_user.is_authenticated:
            return redirect(url_for('user.imoveis'))
        else:
            return redirect(url_for('user.login'))

    app.register_blueprint(user)


    return app