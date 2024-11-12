from flask import Flask, redirect, url_for, render_template

app = Flask(__name__)
a=False

@app.route("/")
def home():
	return render_template("Main.html", title="login")

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