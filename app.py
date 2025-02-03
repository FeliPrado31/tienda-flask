from flask import Flask
from flask_login import LoginManager
from extensions import db
from routes.admin_routes import admin_bp
from routes.cliente_routes import cliente_bp
from routes.auth_routes import auth_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost/ecommerce'


db.init_app(app)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return db.session.get(User, int(user_id))


app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(cliente_bp, url_prefix='/cliente')
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)