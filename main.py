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
from forms import  AddNewOrder, CreatePostForm


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
    product: Mapped[str] = mapped_column(String(250), unique=False, nullable=False)
    amount: Mapped[str] = mapped_column(Integer, nullable=False)
    provider: Mapped[str] = mapped_column(String(250), nullable=False)
    product_url: Mapped[str] = mapped_column(String(250), nullable=False)
    user: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)
    delivery_date: Mapped[str] = mapped_column(String(250), nullable=True)


class Ideas(db.Model):
    __tablename__ = "ideas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    subtitle: Mapped[str] = mapped_column(String(250), unique=True, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    author: Mapped[str] = mapped_column(String(250), nullable=False)
    date: Mapped[str] = mapped_column(String(250), nullable=False)


with app.app_context():
    db.create_all()


# Creating the Routes to the different pages
@app.route("/")
def home():
    return render_template("index.html")

@app.route('/make-order', methods = ["POST", "GET"])
def make_order():
    form = AddNewOrder()
    if form.validate_on_submit():
        new_post = Orders(
            product=form.product.data,
            amount=form.amount.data,
            provider=form.provider.data,
            product_url=form.product_url.data,
            user=form.user.data,
            date=datetime.date.today().strftime("%B %d, %Y"),
            delivery_date = "not delivered"
        )
        db.session.add(new_post)
        db.session.commit()
        # return redirect(url_for("get_all_posts"))
        return redirect(url_for("pending_orders"))
    return render_template("make_order.html", form=form)

@app.route('/all_orders', methods = ["GET", "POST"])
def all_orders():
    result = db.session.execute(db.select(Orders))
    posts = result.scalars().all()
    return render_template("orders.html", all_posts=posts)

@app.route('/pending_orders', methods = ["GET", "POST"])
def pending_orders():
    result = db.session.execute(db.select(Orders))
    posts = result.scalars().all()
    pending = []
    for post in posts:
        if post.delivery_date == "not delivered":
            pending.append(post)


    return render_template("pending_orders.html", all_posts=pending)

@app.route('/show_order/<int:order_id>', methods = ["POST", "GET"])
def show_order(order_id):
        post = db.get_or_404(Orders, order_id)
        return render_template("show_order.html", order = post, order_id = post.id)

@app.route('/edit_order/<int:order_id>', methods = ["POST", "GET"])
def edit_order(order_id):
    order = db.get_or_404(Orders, order_id)
    edit_form = AddNewOrder(
        product=order.product,
        amount=order.amount,
        provider=order.provider,
        product_url=order.product_url,
        user=order.user,
        delivery_date = datetime.date.today().strftime("%B %d, %Y"),
    )

    if edit_form.validate_on_submit():
        order.product = edit_form.product.data
        order.amount = edit_form.amount.data
        order.provider = edit_form.provider.data
        order.product_url = edit_form.product_url.data
        order.user = edit_form.user.data
        order.delivery_date = datetime.date.today().strftime("%B %d, %Y")


        db.session.commit()

        return redirect(url_for("all_orders"))  # order_id =order.id))
    return render_template("make_order.html", form=edit_form, is_edit=True, order_id=order.id)


@app.route("/ideas", methods = ["POST", "GET"])
def post_idea():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = Ideas(
            title = form.title.data,
            subtitle = form.subtitle.data,
            body = form.body.data,
            author = form.author.data,
            date = datetime.date.today().strftime('%B %d, %Y')
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_ideas"))
    return render_template('ideas.html', form = form)

@app.route('/all_ideas')
def get_all_ideas():
    result = db.session.execute(db.select(Ideas))
    ideas = result.scalars().all()
    return render_template('all_ideas.html', all_posts = ideas)



@app.route("/lab_equipment")
def show_lab_equipment():
    return  render_template('lab_equipment.html')


@app.route("/chemicals")
def chemicals():
    return  render_template('chemicals.html')

if __name__ == "__main__":
    app.run(debug=True)

