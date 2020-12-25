from flask import Flask, render_template, request, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def layout():
    return render_template('layout.html')

@app.route('/customer')
def customer():
    return render_template('add_orders.html')

@app.route('/add_customer_button', methods=["POST"])
def  add_customer():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    customerid = request.form.get("customerid")
    company = request.form.get("company")
    address = request.form.get("address")
    name = request.form.get("name")
    contact = request.form.get("contact")
    mailid = request.form.get("mailid")
    
    c.execute("INSERT INTO customer VALUES (?, ?, ?, ?, ?, ?)", (customerid, company, address, name, contact, mailid))
    conn.commit()
    conn.close()

    return "Successful"

@app.route('/order')
def order():
    return render_template('add_orders.html')

@app.route('/add_orders_button', methods=["POST"])
def  add_orders():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    orderid = request.form.get("orderid")
    customerid = request.form.get("customerid")
    orderdate = request.form.get("orderdate")
    productname = request.form.get("productname")
    productid = request.form.get("productid")
    description = request.form.get("description")
    estimatedcost = request.form.get("estimatedcost")
    deadline = request.form.get("deadline")
    
    c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)",(orderid, customerid, orderdate, productname, productid, description, estimatedcost, deadline))
    conn.commit()
    conn.close()
    
    return render_template("")


@app.route('/rawmaterial')
def rawmaterial():
    return render_template('add_rawmaterials.html')

@app.route('/add_rawmaterials_button', methods=["POST"])
def  add_rawmaterials():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    customerid = request.form.get("customerid")
    orderid = request.form.get("orderid")
    materials = request.form.get("materials")
    cost = request.form.get("cost")
    
    c.execute("INSERT INTO rawmaterials VALUES (?, ?, ?, ?, ?, ?)",(customerid, orderid, materials, cost))
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

    customerid = request.form.get("customerid")
    orderid = request.form.get("orderid")
    requireddays = request.form.get("requireddays")
    startdate = request.form.get("startdate")
    enddate = request.form.get("enddate")
    extradays = request.form.get("extradays")
    
    c.execute("INSERT INTO production VALUES (?, ?, ?, ?, ?, ?)",(customerid, orderid, requireddays, startdate, enddate, extradays))
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

    customerid = request.form.get("customerid")
    orderid = request.form.get("orderid")
    weight = request.form.get("weight")
    shippingaddress = request.form.get("shippingaddress")
    transportationtype = request.form.get("transportationtype")
    
    c.execute("INSERT INTO shipment VALUES (?, ?, ?, ?, ?, ?)",(customerid, orderid, weight, shippingaddress, transportationtype))
    conn.commit()
    conn.close()
    
    return render_template("")