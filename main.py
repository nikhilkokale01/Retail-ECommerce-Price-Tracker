from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import mysql.connector
import hashlib
import os
from bs4 import BeautifulSoup
import requests
import re

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configuration for MySQL connection
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'DScl@123',
    'database': 'pricetracker'
}

# Function to fetch products based on category
def fetch_products(category):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product WHERE category = %s", (category,))
        products = cursor.fetchall()
        return products
    except mysql.connector.Error as err:
        print("Error:", err)
        return []

# Function to fetch product details by ID
def fetch_product_by_id(product_id):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM product WHERE product_id = %s", (product_id,))
        product = cursor.fetchone()
        return product
    except mysql.connector.Error as err:
        print("Error:", err)
        return None
      
def update_prices(product_id):
    try:
        print("IN")
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'vijaysales'".format(product_id)
        cursor.execute(query)
        urls = cursor.fetchone()
        url_vijaysales = urls['url']
        print("url:",url_vijaysales)
        if(url_vijaysales):
            print("IN vs")
            r = requests.get(url_vijaysales)
            soup = BeautifulSoup(r.content, 'html.parser') 
            Price_vijaysales = soup.find_all(class_='clsSpecPrc clsWithVSP')
            print("Price:")
            if(Price_vijaysales):
                print("IN")
                Price_vijaysales = int(Price_vijaysales[0].text.strip().replace("Offer Price₹","").replace(",",""))
            else:
                print("IN")
                Price_vijaysales = int(soup.find_all(class_='priceMRP')[0].text[4:].split("M")[0].replace(',',""))
            price2=float(str(Price_vijaysales))
            print("PRICE_EMAIL:",Price_vijaysales)
            query = "HI"
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'vijaysales'".format(float(str(Price_vijaysales).replace(",","")), product_id)
            print(query)
            cursor.execute(query)
            conn.commit()

        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'croma'".format(product_id)
        cursor.execute(query)
        urls = cursor.fetchone()
        url_croma = urls['url']
        if(url_croma):
            print("IN croma")
            r = requests.get(url_croma)
            soup = BeautifulSoup(r.content, 'html.parser') 
            Price_croma = 0
            script_tags = soup.find_all("script")
            for script in script_tags:
                data = script.get_text()
                if("\"price\"" in data):
                    pattern = r'"price"\s*:\s*"(\d+)"'
                    match = re.search(str(pattern), str(data))
                    if match:
                        Price_croma = match.group(1)
                        break
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'croma'".format(float(str(Price_croma).replace(",","")),product_id)
            price1=float(str(Price_croma))
            print("PRICE_EMAIL:",price1)
            cursor.execute(query)
            conn.commit()

        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'reliancedigital'".format(product_id)
        cursor.execute(query)
        urls = cursor.fetchone()
        url_reliance = urls['url']  
        if(url_reliance):
            print("In rd")
            print(url_reliance)
            r = requests.get(url_reliance)
            soup = BeautifulSoup(r.content, 'html.parser') 
            Price_reliance = soup.find(class_='pdp__priceSection__priceListText').text.strip()
            Price_reliance = Price_reliance.replace("Offer Price: ","")
            Price_reliance = Price_reliance.replace("₹","").strip()
            print("Reliance Digital: ₹{}".format(Price_reliance))
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'reliancedigital'".format(float(str(Price_reliance).replace(",","")),product_id)
            cursor.execute(query)
            conn.commit()
        
        
        query = "SELECT url FROM price WHERE product_id = '{}' AND website = 'flipkart'".format(product_id)
        cursor.execute(query)
        urls = cursor.fetchone()
        url_flipkart = urls['url']
        if(url_flipkart):
            print("IN fp")  
            r = requests.get(url_flipkart)
            soup = BeautifulSoup(r.content, 'html.parser') 
            Price_flipkart = soup.find(class_="_30jeq3 _16Jk6d").text.strip().replace("₹","")
            query = "UPDATE price SET Price = {} WHERE product_id = '{}' AND website = 'flipkart'".format(float(str(Price_flipkart).replace(",","")),product_id)
            cursor.execute(query)
            conn.commit()
    except:
        pass

# Function to fetch price details by product ID
def fetch_prices_by_product_id(product_id):
    try:
        update_prices(product_id)
        print(product_id)
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM price WHERE product_id =%s", (product_id,))
        prices = cursor.fetchall()
        print(prices)
        return prices
    except mysql.connector.Error as err:
        print("Error:", err)
        return []

@app.route('/index')
def index():
    if 'username' in session:
        return render_template('index.html')             # return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/products/<category>')
def get_products(category):
    products = fetch_products(category)
    return jsonify(products)

@app.route('/product/<product_id>')
def get_product(product_id):
    product = fetch_product_by_id(product_id)
    if product:
        return jsonify(product)
    else:
        return jsonify({'error': 'Product not found'}), 404
    
@app.route('/price/<product_id>')
def get_prices(product_id):
    prices = fetch_prices_by_product_id(product_id)
    return jsonify(prices)

# Login
# Function to register a new user
def register_user(username, password, email, first_name, last_name, phone_number):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("INSERT INTO user (username, passwd, email, first_name, last_name, phone_number) VALUES (%s, %s, %s, %s, %s, %s)",
                       (username, hashed_password, email, first_name, last_name, phone_number))
        conn.commit()
        return True
    except mysql.connector.Error as err:
        print("Error:", err)
        return False

# Function to authenticate user login
def authenticate_user(username, password):
    try:
        conn = mysql.connector.connect(**mysql_config)
        cursor = conn.cursor()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT * FROM user WHERE username = %s AND passwd = %s", (username, hashed_password))
        user = cursor.fetchone()
        if user:
            session['username'] = username
            
           
            return True
        else:
            return False
    except mysql.connector.Error as err:
        print("Error:", err)
        return False
    
@app.route('/')
def landing_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            return redirect(url_for('index'))  # Redirect to index upon successful authentication
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html', error=None)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        phone_number = request.form['phone_number']
        if register_user(username, password, email, first_name, last_name, phone_number):
            return redirect(url_for('login'))
        else:
            return render_template('register.html', error='Registration failed')
    return render_template('register.html', error=None)

@app.route('/logout',methods=['GET', 'POST'])
def logout():
    session.pop('username', None)  # Remove the username from the session if it exists
    return redirect(url_for('login'))  # Redirect to the login page after logout
    # return render_template('login.html', error=None)

@app.route('/add_to_watchlist/<product_id>', methods=['POST'])
def add_to_watchlist(product_id):
    print("In watchlist:")
    conn = mysql.connector.connect(**mysql_config)
    cursor = conn.cursor(dictionary=True)
    
    # Fetch user_id from the session using the username
    username = session.get('username')

    print("Username:")
    print(username)
    if username:
        cursor.execute("SELECT user_id FROM user WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            user_id = user['user_id']
            print("User ID:", user_id)
            # Proceed with adding the product to the watchlist
            query = "SELECT MIN(Price) AS min_price FROM price WHERE product_id = %s"
            cursor.execute(query, (product_id,))
            min_price = cursor.fetchone()['min_price']
            print("Min-Price:", min_price)
            
            print("Inserting into watchlist:")
            cursor.execute("INSERT INTO watchlist (user_id, product_id, original_price) VALUES (%s, %s, %s)",
               (user_id, product_id, min_price))
            conn.commit()
            print("Added to watchlist successfully")
            return jsonify({"success": True}), 200
    else:
        print("User not authenticated.")
        return jsonify({"error": "User not authenticated."}), 401

if __name__ == '__main__':
    app.run(debug=True)
