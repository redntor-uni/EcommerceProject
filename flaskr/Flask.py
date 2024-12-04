from flask import Flask, redirect, request, url_for, render_template, session, jsonify, flash
from datetime import datetime
import mysql.connector
import stripe, os



app = Flask(__name__)
app.secret_key = 'pathfinders_key'  # For session management

stripe.api_key = 'sk_test_51QSMXlAx0M62oNutLaFPOZBmhxzAUPhuJFoKEUVIDyFmcpWWLvczpY4cIl3yOBr67Kpp9AOP5kx6L1k49cqNBuAy003cRWRzNL'
STRIPE_PK = 'pk_test_51QSMXlAx0M62oNutidvR8YzmC4Gbn4ubnDeMNXAGq9I8UE46h8CSvfvmOMaxsynLxgfLe7PA3OeEFWareAdaEzpA00vJIiJNmG'


# Connect to MySQL database -------------------------------------------------------------------------------------------------------------------------
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="redentor",
    database="pathfinders"
)

cursor = db.cursor(dictionary=True)
query = "SELECT * FROM Products "
cursor.execute(query)
Products = cursor.fetchall()
#-------------------- API-ROUTES-WITH-DEFINITIONS -----------------------------------------------------------------------------------------------------
@app.route('/api/Products')
def get_products():
    return jsonify({"Products": Products})

@app.route('/api/Products/search')
def search_products():
    query = request.args.get('query', '').lower()
    matching_products = []
    if query:
        matching_products = [p for p in Products if query in p['Name'].lower()]
    return jsonify({"results": matching_products})

@app.route('/api/add_to_cart/<pid>', methods=['POST'])
def add_to_cart(pid):
    init_cart()
    matching_product = [p for p in Products if int(pid) == p['id']]
    quantity = 1
    if pid in session['cart']:
        session['cart'][pid] += quantity
    else:
        session['cart'][pid] = quantity
    session.modified = True
    return jsonify({})

def init_cart():
    if 'cart' not in session:
        session['cart'] = {}
def init_order():
    if 'order' not in session:
        session['order'] = {}
#-------------------- NORMAL-ROUTES-WITH-DEFINITIONS -----------------------------------------------------------------------------------------------------
#------------------- restructured-according-to-NavBar ----------------------------------------------------------------------------------------------------

@app.route("/")
def home():
    if 'username' in session and session['username'] is not None:
        username = session['username']
        welcome = f"Welcome {username}! You are signed in."
    else:
        welcome = "Welcome to our website, where you can shop stylish shoes."
    return render_template("Main.html", welcome=welcome, logged_in='username' in session)

@app.route("/Products")
def products(pid=None):
    if pid is None:
        return render_template("Products.html", logged_in='username' in session)
    matching_product = [p for p in Products if int(pid) == p['ID']]
    return render_template('Product_Item.html', Products=matching_product[0], logged_in='username' in session)

@app.route("/Contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        email = request.form['email']
        message = request.form['message']
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"insert into Contact (Email, Message) values ('{email}', '{message}')")
        db.commit()
        cursor.close()
        success_message = "Submitted Succesfully! We will reach out via email soon with a response."
        return render_template("Contact_Us.html", success = success_message, logged_in='username' in session)

    return render_template("Contact_Us.html", logged_in='username' in session)

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
            return render_template('login.html', error="Invalid credentials, please try again.")
    
    return render_template('login.html')

@app.route("/Register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        
        cursor = db.cursor(dictionary=True)
        cursor.execute(f"insert into Users (User, Password, Email) values ('{username}', '{password}', '{email}')")
        db.commit()
        cursor.close()
        return redirect(url_for('login'))
    return render_template("Register.html")

@app.route("/Logout")
def logout():
	session.clear()
	return redirect(url_for('home'))

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

@app.route("/Cart")
# def cart():
#     cursor = db.cursor(dictionary=True)
#     query = "SELECT * FROM Carts c join Products p on c.ItemID = p.ID WHERE c.Status = %s  AND UserID = %s "
#     cursor.execute(query, ('Active', session['UserID']))
#     cart = cursor.fetchall()

#     init_cart()
#     cart_items = []
#     total = 0
#     # cart = session['cart']
#     if cart:
#         # Access properties of the cart
#         for item in cart:
#             print(f"Product ID: {item['ItemID']}, Quantity: {item['Quantity']}, Price: {item['Price']}")
#             item_total = item['Quantity'] * item['Price']
#             cart_items.append({
#                 'id': item['ItemID'],
#                 'name': item['Name'],
#                 'description' : item['Description'],
#                 'price': item['Price'],
#                 'quantity': item['Quantity'],
#                 'imgURL': item['Img'],
#                 'total': item_total
#             })
#             total += item_total

#     return render_template("Cart.html", cart_items=cart_items, total=total, logged_in='username' in session)

def cart():
    if 'username' in session and session['username'] is not None:
        init_cart()
        cart = session['cart']
        cart_items = []
        total = 0
        for pid, qty in cart.items():
            product = [p for p in Products if int(pid) == p['ID']][0]
            if product:
                item_total = product['price'] * qty
                cart_items.append({
                    'id': pid,
                    'image': product['image'],
                    'name': product['name'],
                    'price': product['price'],
                    'quantity': qty,
                    'total': item_total
                })
                total += item_total
        return render_template('cart.html', cart_items=cart_items, total=total, logged_in='username' in session)
    else:
        return redirect(url_for('login'))

@app.route("/OrderCompleted", methods=['GET','POST'])
def orderCompleted():

    # Get the items from the form data
    # items = request.form.getlist('items[]')  # Get the list of items from the hidden inputs

    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Carts c join Products p on c.ItemID = p.ID WHERE c.Status = %s  AND UserID = %s "
    cursor.execute(query, ('Active', session['UserID']))
    cart = cursor.fetchall()

    # Parse the item details (name, quantity, price) from the string
    parsed_items = []
    total = 0
    if cart:
        
        # for item in items:
        #     id, name, quantity, price = item.split('|')
        #     parsed_items.append({
        #         'id': id,
        #         'name': name,
        #         'quantity': int(quantity),
        #         'price': float(price),
        #         'total': int(quantity) * float(price)
        #     })
        #     total += int(quantity) * float(price)
        
        for item in cart:
            print(f"Product ID: {item['ID']}, Quantity: {item['Quantity']}, Price: {item['ItemPrice']}")
            item_total = item['Quantity'] * item['Price']
            parsed_items.append({
                'id': item['ID'],
                'name': item['Name'],
                # 'description' : item['Description'],
                'price': float(item['Price']),
                'quantity': int(item['Quantity']),
                # 'item_total': item_total,
                # 'imgURL': item['Img'],
                'total': item_total
            })
            total += item_total 
        
        
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


    return render_template("Cart.html", cart_items=cart_items, total=total, logged_in='username' in session, public_key=STRIPE_PK)


@app.route('/payment', methods=['POST'])
def create_and_confirm_payment():
    
    cursor = db.cursor(dictionary=True)
    query = "SELECT * FROM Carts c join Products p on c.ItemID = p.ID WHERE c.Status = %s  AND UserID = %s "
    cursor.execute(query, ('Active', session['UserID']))
    cart = cursor.fetchall()
    
    if cart:
        # Get data from the form
        data = request.json
        cart_items = []
        for item in cart:
            cart_items.append({
                'price_data': {
                    'currency': data.get('currency', 'usd'),
                    'product_data': {
                        'name': item['Name'],
                    },
                    # 'unit_amount': item['Price'] * 100, # Amount in cents
                    'unit_amount_decimal': item['Price'] * 100,
                },
                'quantity': item['Quantity'],
            })
        checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                mode='payment',
                line_items=cart_items,
                success_url='http://localhost:5001/OrderCompleted',
                cancel_url='http://localhost:5000/cancel',
            )
        return jsonify({'id': checkout_session.id})
    return redirect(url_for('checkout'))




if __name__ == '__main__':
	app.run(debug=True, port=5001)