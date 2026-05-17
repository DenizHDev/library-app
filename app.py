from flask import Flask, render_template, request,redirect, flash, session
from flask_bcrypt import Bcrypt
import database


app = Flask(__name__)
app.secret_key = "your_secret_key"
database.create_tables()
app.config["SESSION_PERMANENT"] = False
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("index.html",books=database.get_available_books(session["user_id"]), checked_books=database.get_checked_books(session["user_id"]))

@app.route("/add",methods=["POST"])
def add_book():
    title = request.form["book_title"]
    author = request.form["book_author"]
    pages = request.form["book_pages"]
    if database.add_book(title,author,pages,session["user_id"]):
        flash("Book added successfully!", "success")
        return redirect("/")
    else:
        flash("Book is already in the library!", "danger")
        return redirect("/")

@app.route("/checkout", methods=["POST"])
def checkout_book():
    title = request.form["title"]
    database.checkout_book(title)
    return redirect("/")

@app.route("/remove", methods=["POST"])
def remove_book():
    title = request.form["title"]
    database.remove_book(title)
    return redirect("/")

@app.route("/return", methods=["POST"])
def return_book():
    title = request.form["title"]
    database.return_book(title)
    return redirect("/")

@app.route("/register", methods = ["POST","GET"])
def register():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        email = request.form["email"]
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
        if database.register_user(username, email, hashed_password):
            flash("User successfully registered!", "success")
            return redirect("/login")

        else:
            flash("User already exist!", "danger")
            return redirect("/register")

    return render_template("register.html")

@app.route("/login", methods = ["POST","GET"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = database.get_user(username)
        if user and bcrypt.check_password_hash(user[3],password):
            session.permanent = False
            session["user_id"] = user[0]
            session["username"] = user[1]
            flash("You have successfully logged in!", "success")
            return redirect("/")
        else:
            flash("User doesn't exist!","danger")
            return redirect("/login")
    return render_template("login.html")

@app.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been logged out!", "success")
    return redirect("/login")


if __name__=="__main__":
    app.run(debug=True)