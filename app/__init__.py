from flask import Flask
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_moment import Moment 


app = Flask(__name__)
app.config.from_object(Config)


db = SQLAlchemy(app)
migrate = Migrate(app,db)
moment =  Moment()
login = LoginManager(app=app)
login.login_view = "login"
login.login_message = "You are not authorized to view this page"

@app.shell_context_processor
def make_admin_shell_context():
    return {
        "db" : db
    }


from app import routes
from app.models import schema
