from datetime import datetime
from apps.app import db, login_master
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Item(db.Model):

    __tablename__ = "Items"

    id=db.Column(db.Integer, primary_key=True) #물품 고유 번호
    itemname=db.Column(db.String, unique=True, index=True)#물품 이름
    item_quantity=db.Column(db.Integer)#물품 수량
    time=db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)#입고 날짜
    item_description = db.Column(db.String)#물품 설명

class Representative(db.Model,UserMixin):

    __tablename__ = "Representative"

    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, index=True)
    useremail = db.Column(db.String, unique=True, index=True)
    password_hash = db.Column(db.String)

    @property
    def password(self):
        raise AttributeError("읽어 드릴 수 없음")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_duplicate_email(self):
        return Representative.query.filter_by(useremail=self.useremail).first() is not None
    
@login_master.user_loader
def load_user(user_id):
    return Representative.query.get(user_id)

class Log(db.Model):
    __tablename__ ="Log"

    log_id=db.Column(db.Integer, primary_key=True) #순서
    log_itemname=db.Column(db.String, index=True)#물품 이름
    log_item_quantity=db.Column(db.Integer)#제품 수량 변경값 (+-)
    log_item_quantity_now=db.Column(db.Integer)#제품 물품 수량
    log_time=db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)#실시 시간
    log_representative=db.Column(db.String)