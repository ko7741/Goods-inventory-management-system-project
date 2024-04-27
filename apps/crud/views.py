from flask import Blueprint, render_template,redirect,url_for
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
            log_time=datetime.now()
        )
        db.session.add(item)
        db.session.add(log)
        db.session.commit()
        return redirect(url_for("crud.goods"))
    return render_template("crud/create.html", form=form)

@crud.route("/goods")
@login_required
def goods():
    goods=Item.query.all()
    logs=Log.query.all()
    return render_template("crud/goods.html", goods = goods, logs=logs)

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

    
# @crud.route("/goods/<goods_itemname>/delete", methods=["POST"])
# def delete_goods(goods_itemname):
#     item = Item.query.filter_by(itemname=goods_itemname).first()
#     db.session.delete(item)
#     db.session.commit()
#     return redirect(url_for("url_for(crud.goods)"))

