from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired, URL, InputRequired, length, Email
from flask_ckeditor import CKEditorField



# WTF for adding New Orders
class AddNewOrder(FlaskForm):
    product = StringField("Product Name", validators=[DataRequired()])
    amount = StringField("Quantity", validators=[DataRequired()])
    provider = StringField("Provider", validators=[DataRequired()])
    product_url = StringField("Product URL", validators=[DataRequired(), URL()])
    user = StringField("Person who ordered", validators=[DataRequired()])
    submit = SubmitField("Add Order")

# Edit Orders

# for creating new ideas
class CreatePostForm(FlaskForm):
    title = StringField("Idea Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    body = CKEditorField("Blog Content", validators=[DataRequired()])
    author = StringField("Who submitted", validators=[DataRequired()])
    submit = SubmitField("Submit Post")