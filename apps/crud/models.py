from datetime import datetime
from apps.app import db
from werkzeug.security import generate_password_hash

class Item(db.Model):

    __tablename__ = "Items"

    id=db.Column(db.Integer, primary_key=True) #물품 고유 번호
    itemname=db.Column(db.String, unique=True, index=True)#물품 이름
    item_quantity=db.Column(db.Integer)#물품 수량
    in_time=db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)#입고 날짜
    out_time=db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)#출고 날짜
    item_description = db.Column(db.String)#물품 설명

class Representative(db.Model):

    __tablename__ = "Representative"

    username = db.Column(db.String, index=True, primary_key=True)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError("읽어 드일 수 없음")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    