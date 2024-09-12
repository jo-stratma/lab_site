from flask import Flask, render_template
from flask_bootstrap import Bootstrap5
import datetime as datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)


@app.route("/")
def home():
    return render_template("index.html")

@app.route('/test')
def show_testpage():
    return render_template("test.html", date = datetime.datetime.today().strftime("%Y-%m-%d"))

if __name__ == "__main__":
    app.run(debug=True)

