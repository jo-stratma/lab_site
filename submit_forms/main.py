from flask import Flask, render_template, request
import smtplib
MY_EMAIL = "johmh85@gmail.com"
MY_PASSWORD = "ojak wrql qzdg npzb"

with smtplib.SMTP("smtp.gmail.com",  587) as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL,
                        to_addrs="johan.streetman@yahoo.com",
                        msg=f"Subject:Happy Birthday\n\n{birthday_letter}"
                        )


app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST"])
def receive_data():
    email = request.form["email"]
    pword = request.form["password"]
    return f"<h1> Mail: {email}, Password: {pword}"


if __name__ == "__main__":
    app.run(debug=True)