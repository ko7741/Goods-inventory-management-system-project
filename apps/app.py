from flask import Flask
from pathlib import Path
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db=SQLAlchemy()
csrf=CSRFProtect()

def create_app():
    app=Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY="QW123QAWDAXD3221",
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{Path(__file__).parent.parent / 'local.sqlite'}",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True,
        WTF_CSRF_SECRET_KEY='AuwzysU5sugKN7KZs6f',
    )

    db.init_app(app)
    Migrate(app,db)
    csrf.init_app(app)
    
    from apps.crud import views as crud_views
    app.register_blueprint(crud_views.crud, url_prefix="/crud")
    
    return app
