from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap5
import datetime as datetime

from flask_ckeditor import CKEditor

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash


# Import your forms from the forms.py
from forms import  AddNewOrder


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
CKEditor(app)



#TODO Create a Database
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(model_class=Base)
db.init_app(app)

class Orders(db.Model):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    amount: Mapped[str] = mapped_column(Integer, nullable=False)
    provider: Mapped[str] = mapped_column(String(250), nullable=False)
    product_url: Mapped[str] = mapped_column(String(250), nullable=False)
    user: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)

with app.app_context():
    db.create_all()


# Creating the Routes to the different pages
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/orders', methods = ["POST", "GET"])
def add_order():
    form = AddNewOrder()
    if form.validate_on_submit():
        new_post = Orders(
            product=form.product.data,
            amount=form.amount.data,
            provider=form.provider.data,
            product_url=form.product_url.data,
            user=form.user.data,
            date=datetime.date.today().strftime("%B %d, %Y")
        )
        db.session.add(new_post)
        db.session.commit()
        # return redirect(url_for("get_all_posts"))
        return redirect(url_for("home"))
    return render_template("orders.html", form=form)





if __name__ == "__main__":
    app.run(debug=True)

