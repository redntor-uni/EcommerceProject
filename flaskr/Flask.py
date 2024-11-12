from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)

@app.route("/Main/")
@app.route("/")
def home():
	return render_template("Main.html")

@app.route("/Login")
def login():
	return render_template("Login.html")

@app.route("/Contact")
def contact():
	return render_template("Contact_Us.html")

@app.route("/Forgot")
def forgot():
	return render_template("Forgot.html")

@app.route("/Register")
def register():
	return render_template("Register.html")

@app.route("/Cart")
def cart():
	return render_template("Cart.html")

# @app.route("/<name>")
# def user(name):
# 	return f"Hello {name}!"

# @app.route("/admin")
# def admin():
# 	if a:
# 		return "admin"
# 	return redirect(url_for("home"))

if __name__ == '__main__':
	app.run(debug=True)