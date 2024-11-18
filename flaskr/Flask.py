from flask import Flask, jsonify, redirect, request, url_for, render_template, session, flash

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

products = [
    {"id": 1, "name": "Xbox 360", "price": 100},
    {"id": 2, "name": "Play Station 1", "price": 50},
    {"id": 4, "name": "Play Station 2", "price": 70},
    {"id": 5, "name": "Play Station 3", "price": 150},
    { "id": 6, "name": "Laptop", "price": 899 },
    { "id": 7, "name": "Smartphone", "price": 699 },
    { "id": 8, "name": "Headphones", "price": 199 },
    { "id": 9, "name": "Smartwatch", "price": 299 },
    { "id": 10, "name": "Tablet", "price": 399 },
    { "id": 11, "name": "Camera", "price": 499 },
    { "id": 12, "name": "Printer", "price": 149 },
    { "id": 13, "name": "Monitor", "price": 229 },
    { "id": 14, "name": "Keyboard", "price": 79 },
    { "id": 15, "name": "Mouse", "price": 49 }
]

def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

@app.route('/api/products')
def get_products():
    return jsonify({"products": products})

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
            session['UserID'] = user['ID']
            return redirect(url_for('home'))
        else:
            return "Invalid credentials, please try again."
    
    return render_template('login.html')

@app.route("/Products")
@app.route("/Products/<pid>")
def products(pid=None):
    if pid is None:
        return render_template("Products.html", logged_in='username' in session)
    matching_product = [p for p in products if int(pid) == p['id']]
    return render_template('Product_Item.html', product=matching_product[0], logged_in='username' in session)

@app.route("/Contact")
def contact():
	return render_template("Contact_Us.html", logged_in='username' in session)

@app.route("/Settings")
def settings():
    if 'username' in session and session['username'] is not None:
        username = session['username']
        return render_template("Settings.html", username=session['username'], logged_in='username' in session)
    else:
        return redirect(url_for('login'))

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
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Carts c join Products p on c.ItemID = p.ID WHERE UserID = %s "
    cursor.execute(query, (session['UserID'],))
    cart = cursor.fetchall()

    init_cart()
    cart_items = []
    total = 0
    # cart = session['cart']
    if cart:
        # Access properties of the cart
        for item in cart:
            print(f"Product ID: {item['ItemID']}, Quantity: {item['Quantity']}, Price: {item['Price']}")
            item_total = item['Quantity'] * item['Price']
            cart_items.append({
                'id': item['ItemID'],
                'name': item['Name'],
                'description' : item['Description'],
                'price': item['Price'],
                'quantity': item['Quantity'],
                'imgURL': item['Img'],
                'total': item_total
            })
            total += item_total
        # for pid, qty in cart.items():
        #     product = [p for p in products if int(pid) == p['id']][0]
        #     if product:
        #         item_total = product['price'] * qty
        #         cart_items.append({
        #             'id': pid,
        #             'name': product['name'],
        #             'price': product['price'],
        #             'quantity': qty,
        #             'total': item_total
        #         })
        #         total += item_total

    return render_template("Cart.html", cart_items=cart_items, total=total)

if __name__ == '__main__':
	app.run(debug=True, port=5001)