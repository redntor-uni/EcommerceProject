from flask import Flask, redirect, request, url_for, render_template, session
import mysql.connector



app = Flask(__name__)
app.secret_key = 'pathfinders_key'  # For session management

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="EddieO0528",
    database="pathfinders"
)

@app.route("/Main/")
@app.route("/")
def home():
	return render_template("Main.html", logged_in='username' in session)

@app.route("/Login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM Users WHERE User = %s AND Password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        if user:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

@app.route("/Products")
def products():
	return render_template("Products.html")

@app.route("/Products/Product_Item")
def product_item():
	return render_template("Product_Item.html")

@app.route("/Contact")
def contact():
	return render_template("Contact_Us.html")

@app.route("/Forgot")
def forgot():
	return render_template("Forgot.html")

@app.route("/Logout")
def logout():
	session.clear()
	return redirect(url_for('home'))


@app.route("/Register")
def register():
	return render_template("Register.html")

@app.route("/Cart")
def cart():
	return render_template("Cart.html")

if __name__ == '__main__':
	app.run(debug=True, port=5001)