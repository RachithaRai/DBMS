from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)

username = 'admin'
password = 'admin'


@app.route('/option/<string:cat>')
def option(cat):
    return render_template('option.html', option=cat)

@app.route('/')
def layout():
    return render_template('login.html')


@app.route('/signup')
def client_signup():
    return render_template('signup.html')

@app.route('/signup_button', methods=["POST"])
def  clientdetails():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    
    clientusername = request.form.get("clientusername")
    password = request.form.get("password")
    name = request.form.get("name")
    company = request.form.get("company")
    contact = request.form.get("contact")
    mailid = request.form.get("mailid")
    address = request.form.get("address")
    
    c.execute("INSERT INTO client (clientusername, password, company, address, name, contact, mailid) VALUES(?, ?, ?, ?, ?, ?, ?)", (clientusername, password, company, address, name, contact, mailid) )
    conn.commit()
    conn.close()

    return "Successful"


@app.route('/login')
def clientlogin():
    return render_template('login.html')

@app.route('/client_login_button', methods=["POST"])
def  addclient():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    clientusername = request.form.get("clientusername")
    password = request.form.get("password")
    
    c.execute("INSERT INTO client VALUES (?, ?)", (clientusername, password))
    conn.commit()
    conn.close()

    return "Successful"

@app.route('/admin_login_button', methods=["POST"])
def admin():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    adminusername = request.form.get("adminusername")
    adminpassword = request.form.get("password")
   
    if adminusername==username and adminpassword==password:
        return render_template('category.html')

@app.route('/client')
def client():
    return render_template('add_orders.html')

@app.route('/add_client_button', methods=["POST"])
def  add_client():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    clientid = request.form.get("clientid")
    company = request.form.get("company")
    address = request.form.get("address")
    name = request.form.get("name")
    contact = request.form.get("contact")
    mailid = request.form.get("mailid")
    
    c.execute("INSERT INTO client VALUES (?, ?, ?, ?, ?, ?)", (clientid, company, address, name, contact, mailid))
    conn.commit()
    conn.close()

    return "Successful"

@app.route('/orders')
def order():
    return render_template('add_orders.html')

@app.route('/add_orders_button', methods=["POST"])
def  add_orders():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    orderid = request.form.get("orderid")
    clientid = request.form.get("clientid")
    orderdate = request.form.get("orderdate")
    productname = request.form.get("productname")
    productid = request.form.get("productid")
    description = request.form.get("description")
    estimatedcost = request.form.get("estimatedcost")
    deadline = request.form.get("deadline")

    c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)",(orderid, clientid, orderdate, productname, productid, description, estimatedcost, deadline)) 

    conn.commit()
    conn.close()
    return render_template("orders.html")

@app.route('/vieworders')
def render_all_orders():
    with sqlite3.connect('file.db') as conn:
        c = conn.cursor()

        orders_query = c.execute("""SELECT * FROM orders""").fetchall()

        return render_template("orders.html", orders=orders_query)


@app.route('/rawmaterial')
def rawmaterial():
    return render_template('add_rawmaterials.html')

@app.route('/add_rawmaterials_button', methods=["POST"])
def  add_rawmaterials():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    clientid = request.form.get("clientid")
    orderid = request.form.get("orderid")
    materials = request.form.get("materials")
    cost = request.form.get("cost")
    
    c.execute("INSERT INTO rawmaterials VALUES (?, ?, ?, ?)",(clientid, orderid, materials, cost))
    conn.commit()
    conn.close()
    
    return render_template("")


@app.route('/production')
def production():
    return render_template('add_production.html')


@app.route('/add_production_button', methods=["POST"])
def  add_production():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    clientid = request.form.get("clientid")
    orderid = request.form.get("orderid")
    requireddays = request.form.get("requireddays")
    startdate = request.form.get("startdate")
    enddate = request.form.get("enddate")
    extradays = request.form.get("extradays")
    
    c.execute("INSERT INTO production VALUES (?, ?, ?, ?, ?, ?)",(clientid, orderid, requireddays, startdate, enddate, extradays))
    conn.commit()
    conn.close()
    
    return render_template("")


@app.route('/shipment')
def shipment():
    return render_template('add_shipment.html')

@app.route('/add_shipment_button', methods=["POST"])
def  add_shipment():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    clientid = request.form.get("clientid")
    orderid = request.form.get("orderid")
    weight = request.form.get("weight")
    shippingaddress = request.form.get("shippingaddress")
    transportationtype = request.form.get("transportationtype")
    
    c.execute("INSERT INTO shipment VALUES (?, ?, ?, ?, ?, ?)",(clientid, orderid, weight, shippingaddress, transportationtype))
    conn.commit()
    conn.close()
    
    return render_template("")