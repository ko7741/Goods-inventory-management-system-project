from flask import Blueprint, jsonify, render_template,redirect,url_for,flash,request
from sqlalchemy import JSON
from apps.crud.forms import ItemForm
from apps.app import db
from apps.crud.models import Item,Log
from datetime import datetime
from flask_login import current_user, login_required

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@crud.route("/")
@login_required
def index():
    return render_template("crud/index.html")

@crud.route("/goods/new",methods=["GET","POST"])
@login_required
def create_goods():
    form = ItemForm()
    if form.validate_on_submit():

        item = Item(
            itemname=form.itemname.data,
            item_quantity=form.item_quantity.data,
            time=form.time.data,
            item_description=form.item_description.data,
        )
        log= Log(
            log_itemname=form.itemname.data,
            log_item_quantity=form.item_quantity.data,
            log_item_quantity_now=form.item_quantity.data,
            log_time=form.time.data,
            log_representative = current_user.username
        )
        db.session.add(item)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for("crud.goods"))
    return render_template("crud/create.html", form=form)

@crud.route("/goods")
@login_required
def goods():
    form = ItemForm()
    goods=Item.query.all()
    logs=Log.query.all()
    return render_template("crud/goods.html", goods = goods, logs=logs, form=form)

@crud.route("/goods/<goods_id>", methods=["GET","POST"])
@login_required
def change_quantity(goods_id):
    form = ItemForm()
    goods = Item.query.filter_by(id=goods_id).first()
    if form.validate_on_submit():
        log= Log(
            log_itemname=form.itemname.data,
            log_item_quantity=(form.item_quantity.data-goods.item_quantity),
            log_item_quantity_now=form.item_quantity.data,
            log_time=datetime.now(),
            log_representative = current_user.username
        )
        goods.itemname=form.itemname.data
        goods.item_quantity=form.item_quantity.data
        goods.time=datetime.now()
        goods.item_description=form.item_description.data

        db.session.add(goods)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for("crud.goods"))
    form.item_description.data = goods.item_description
    return render_template("crud/change_quantity.html",item = goods,form=form)

    
@crud.route("/goods/<goods_itemname>/delete", methods=["POST"])
def delete_goods(goods_itemname):
    item = Item.query.filter_by(itemname=goods_itemname).first()
    db.session.delete(item)
    log= Log(
            log_itemname=goods_itemname,
            log_item_quantity=None,
            log_item_quantity_now=None,
            log_time=datetime.now(),
            log_representative = current_user.username,
        )
    db.session.add(log)
    db.session.commit()
    return redirect(url_for("crud.goods"))

@crud.route("/log_delete", methods=["POST"])
def delete_log():
    db.session.query(Log).delete()
    db.session.commit()
    flash("로그가 삭제되었습니다.", "success")
    return redirect(url_for("crud.goods"))

@crud.route("/logvalue", methods=["POST"])
def log_value():
    if request.method == 'POST':
        data = request.json 
        value = data.get('value') 

        if value=="전체":
            logs =Log.query.all()
        else:
            logs =Log.query.filter_by(log_itemname=value).all()

        serialized_logs = []
        for log in logs:
            serialized_log = {
                "log_id": log.log_id,
                "log_itemname": log.log_itemname,
                "log_item_quantity": log.log_item_quantity,
                "log_item_quantity_now": log.log_item_quantity_now,
                "log_time": log.log_time.strftime("%Y-%m-%d %H:%M:%S"),
                "log_representative": log.log_representative
            }
            serialized_logs.append(serialized_log)
        return jsonify(serialized_logs)
            
# @crud.route("/logvalue/<value>")
# def log_value_view(value):
#     print(value)
#     form = ItemForm()
#     goods=Item.query.all()
#     logs=Log.query.filter_by(log_itemname=value).all()
#     print("zz: " , logs)
#     return render_template("crud/goods.html", goods = goods, logs=logs, form=form)
    
    
    

    # data = request.json  # 클라이언트에서 전달된 JSON 데이터를 가져옴
    # value = data.form['value']  # JSON 데이터에서 'value' 키의 값을 가져옴
    # form = ItemForm()
    # goods=Item.query.all()
    # logs=Log.query.filter_by(log_itemname = value).all()
    # return render_template("crud/goods.html", goods = goods, logs=logs, form=form)