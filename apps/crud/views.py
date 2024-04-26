from flask import Blueprint, render_template,redirect,url_for
from apps.crud.forms import ItemFrom
from apps.app import db
from apps.crud.models import Item
from datetime import datetime

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)

@crud.route("/")
def index():
    return render_template("crud/index.html")

@crud.route("/goods/new",methods=["GET","POST"])
def create_goods():
    form = ItemFrom()
    if form.validate_on_submit():

        item = Item(
            itemname=form.itemname.data,
            item_quantity=form.item_quantity.data,
            time=form.time.data,
            item_description=form.item_description.data,
        )
        db.session.add(item)
        db.session.commit()
        return redirect(url_for("crud.goods"))
    return render_template("crud/create.html", form=form)

@crud.route("/goods")
def goods():
    goods=Item.query.all()
    return render_template("crud/goods.html", goods = goods)