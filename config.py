import os 
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "asdfasdasdfsafa45a8935-403494uihfjsdnd"
    SQLALCHEMY_DATABASE_URI =os.environ.get("DATABASE_URL") or "sqlite:///" + os.path.join(basedir, "app.db")
