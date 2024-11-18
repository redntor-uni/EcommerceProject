from flask import Flask, redirect, request, url_for, render_template, session
from datetime import datetime
import mysql.connector



app = Flask(__name__)
app.secret_key = 'pathfinders_key'  # For session management

# Connect to MySQL database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="redentor",
    database="pathfinders"
)

def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

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
            session['UserID'] = user['ID']
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

@app.route("/OrderCompleted", methods=['POST'])
def orderCompleted():

    # Get the items from the form data
    items = request.form.getlist('items[]')  # Get the list of items from the hidden inputs

    # Parse the item details (name, quantity, price) from the string
    parsed_items = []
    total = 0
    if len(items) > 0:
        
        for item in items:
            id, name, quantity, price = item.split('|')
            parsed_items.append({
                'id': id,
                'name': name,
                'quantity': int(quantity),
                'price': float(price),
                'total': int(quantity) * float(price)
            })
            total += int(quantity) * float(price)
        cursor = db.cursor(dictionary=True)
        insertQuery = "INSERT INTO Orders (UserID, OrderTotal, OrderDate) VALUES (%s, %s, %s)"
        order_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(insertQuery, (session['UserID'],total, order_date))
        order_id = cursor.lastrowid
        db.commit()
        update_cart_status_query = """
        UPDATE Carts
        SET Status = 'Completed',
        OrderId = %s
        WHERE UserID = %s
        """
        cursor.execute(update_cart_status_query, (order_id, session['UserID']))
        db.commit()
        user_info_query = """
        SELECT * FROM Users WHERE ID = %s
        """
        cursor.execute(user_info_query, (session['UserID'],))
        user = cursor.fetchone()
        userName = user['User']
        userEmail = user['Email']
        return render_template("OrderCompleted.html", cart_items=parsed_items, total=total, userName=userName, userEmail=userEmail)


@app.route("/Cart")
def cart():
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Carts c join Products p on c.ItemID = p.ID WHERE Status = 'Active' AND UserID = %s "
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


    return render_template("Cart.html", cart_items=cart_items, total=total)

if __name__ == '__main__':
	app.run(debug=True, port=5001)