from flask import Flask, redirect, request, url_for, render_template, session, jsonify, flash
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

Products = [
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

@app.route('/api/Products')
def get_products():
    return jsonify({"Products": Products})

@app.route("/Products")
@app.route("/Products/<pid>")
def products(pid=None):
    if pid is None:
        return render_template("Products.html", logged_in='username' in session)
    matching_product = [p for p in Products if int(pid) == p['id']]
    return render_template('Product_Item.html', Products=matching_product[0], logged_in='username' in session)

def init_cart():
    if 'cart' not in session:
        session['cart'] = {}

def init_order():
    if 'order' not in session:
        session['order'] = {}

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


@app.route('/myOrders')
def myOrders():
    cursor = db.cursor(dictionary=True)
    query = ("SELECT * FROM Orders o JOIN Carts c ON " +
             "c.OrderID = o.ID JOIN Products p ON c.ItemId = p.ID " +
             "WHERE o.UserID = %s ")
    
    cursor.execute(query, (session['UserID'],))
    orders = cursor.fetchall()

    init_order()
    order_items = []
    total = 0

    if orders:
        # Access properties of the cart
        for order in orders:
            print(f"Order ID: {order['OrderID']}, Order Date: {order['OrderDate']}, " +
                  f"Order Total: {order['OrderTotal']} Quantity: {order['Quantity']}, " + 
                  f"Price: {order['ItemPrice']}, Product: {order['Name']}")
            
            item_subtotal = int(order['Quantity']) * float(order['ItemPrice'])
            
            order_items.append({
                'id': order['OrderID'],
                'name': order['Name'],
                # 'description' : item['Description'],
                'price': order['ItemPrice'],
                'quantity': order['Quantity'],
                'itemSubtotal': item_subtotal,
                'imgURL': order['Img'],
                'orderTotal': order['OrderTotal'],
                'orderDate': order['OrderDate'],
                'status': order['Status']
                
            })
            # total += item_total
    return render_template("MyOrders.html", orders=order_items)

@app.route('/updateCart', methods=['POST'])
def updateCart():
    cart_id = request.form.get('cart_id')
    quantity = request.form.get('quantity-' + cart_id)
    price = request.form.get('price')
    # quantity2 = request.form.get('hdnQuantity')
    item_total = int(quantity) * float(price)
    try:
        # Update the cart in the database
        cursor = db.cursor(dictionary=True)
        query = "UPDATE Carts SET Quantity = %s , Total = %s  WHERE ID = %s "
        cursor.execute(query, (quantity, item_total, cart_id))
        db.commit()

        return redirect('/Cart')
        # item = cart
        # if item:
        #     item.quantity = int(quantity)
        #     db.session.commit()
        #     /return jsonify({"success": True, "message": "Cart updated successfully"})
        # else:
        #     return jsonify({"success": False, "message": "Item not found"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)})


@app.route("/Cart")
def cart():
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Carts c join Products p on c.ItemID = p.ID WHERE c.Status = %s  AND UserID = %s "
    cursor.execute(query, ('Active', session['UserID']))
    cart = cursor.fetchall()

    init_cart()
    cart_items = []
    total = 0
    # cart = session['cart']
    if cart:
        # Access properties of the cart
        for item in cart:
            print(f"Product ID: {item['ID']}, Quantity: {item['Quantity']}, Price: {item['ItemPrice']}")
            item_total = item['Quantity'] * item['Price']
            cart_items.append({
                'id': item['ID'],
                'name': item['Name'],
                'description' : item['Description'],
                'price': item['Price'],
                'quantity': item['Quantity'],
                'item_total': item_total,
                'imgURL': item['Img'],
                'total': item_total
            })
            total += item_total


    return render_template("Cart.html", cart_items=cart_items, total=total, logged_in='username' in session)

if __name__ == '__main__':
	app.run(debug=True, port=5001)