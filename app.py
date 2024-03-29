from flask import Flask, render_template, request, url_for, redirect, session
import sqlite3
from datetime import datetime
app = Flask(__name__)

app.secret_key = ('secret key')

ausername = 'admin'
apassword = 'admin'


@app.route('/option/<string:cat>')
def option(cat):
    return render_template('option.html', option=cat)


@app.route('/')
def layout():
    return render_template('layout.html')#login layout

# @app.route('/signin')
# def signin():
#     return render_template('signin.html')

# ``````````````````````````````````````````````````````````````````````````````````````````````````````

# ```````````````````````````````````SIGNUP```````````````````````````````````````````````````````````````````
# @app.route('/category')
# def category():
#     return render_template('category.html')


@app.route('/signup')
def client_signup():
    return render_template('signup.html')

# @app.route('/signout')
# def client_signup():
#     return render_template('signup.html')

@app.route('/signup_button', methods=["POST"])
def  clientdetails():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    
    clientid = request.form.get("clientid")
    clientusername = request.form.get("clientusername")
    password = request.form.get("password")
    name = request.form.get("name")
    company = request.form.get("company")
    contact = request.form.get("contact")
    mailid = request.form.get("mailid")
    address = request.form.get("address")
    
    c.execute("INSERT INTO client (clientid, clientusername, password, company, address, name, contact, mailid) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (clientid, clientusername, password, company, address, name, contact, mailid) )
    conn.commit()
    conn.close()

    # return redirect('/clientdisplay/{}'.format(clientusername))
    return redirect('/signin')
# ``````````````````````````````````````````````````````````````````````````````````````````````````````

# ```````````````````````````````````LOGIN```````````````````````````````````````````````````````````````````
@app.route('/signin')
def signin():
    return render_template('signin.html')


@app.route('/admin_login_button', methods=["POST", "GET"])
def admin():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    user = request.form.get("adminusername")
    adminpassword = request.form.get("password")
 

    post = c.execute("SELECT * FROM client WHERE clientusername=? and password=?", (user, adminpassword)).fetchone() 

    if user == ausername and adminpassword == apassword:
        session['admin'] = user
        print(session['admin'])
        return render_template('category.html')
    elif post != None:
        session['client'] = user
        print(session['client'])
        return redirect('/display/{}'.format(session['client']), )
    else:
        return'nodata'
    # if 'user' in session:
    #     user = session['user']
    #     return render_template('category.html')
    

@app.route('/clientdisplay/<string:clientusername>')
def display(clientusername):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    print(clientusername)


    q = c.execute("""SELECT clientid, clientusername, company, address, name, contact, mailid
                    FROM client WHERE clientusername=?""", (clientusername, )).fetchall()
    print(q)
    conn.commit()
    conn.close()
    return render_template('clientdisplay.html', clients=q)
    # return "hello"


@app.route('/display/<string:clientusername>')
def displayclientorder(clientusername):
    if 'client' in session:
        conn = sqlite3.connect('file.db')
        c = conn.cursor()
        print(clientusername)


        q = c.execute("""SELECT c.clientid, c.clientusername, o.orderid, o.orderdate, p.startdate, p.enddate, s.shipping_address
                        FROM client c, orders o, production p, shipment s 
                        WHERE c.clientusername=? AND c.clientid=o.clientid AND c.clientid=p.clientid AND c.clientid=s.clientid 
                        AND o.orderid=p.orderid AND o.orderid=s.orderid """, (clientusername, )).fetchall()
        # print(q)
        conn.commit()
        conn.close()
        print (q)
        return render_template('clientdisplay.html', clients=q)


    
@app.route('/user')
def user():    
    if 'user' in session:
        user = session['user']
        return render_template('category.html')
    else:
        return redirect('/signin')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return 'logged out'


@app.route('/client')
def client():
    return render_template('add_orders.html')

@app.route('/add_client')
def  add_client():
    return render_template('add_client.html')
@app.route('/add_client_button', methods=["POST"])
def  add_client_button():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    clientid = request.form.get("clientid")
    company = request.form.get("company")
    address = request.form.get("address")
    name = request.form.get("name")
    contact = request.form.get("contact")
    mailid = request.form.get("mailid")
    username = request.form.get("username")
    password = request.form.get("password")

    
    c.execute("INSERT INTO client VALUES (?, ?, ?, ?, ?, ?, ?,?)", (clientid, username, password, company, address, name, contact, mailid))
    conn.commit()
    conn.close()

    return "Successful"
# ``````````````````````````````````````````````````````````````````````````````````````````````````````

# ``````````````````````````````````````ORDER````````````````````````````````````````````````````````````````
@app.route('/addorders')
def order():
    return render_template('add_orders.html')

@app.route('/add_orders_button', methods=["POST"])
def  add_orders():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    x = datetime.now()
    orderid = request.form.get("orderid")
    clientid = request.form.get("clientid")
    orderdate = "{}-{}-{}".format( x.day, x.month, x.year)
    productname = request.form.get("productname")
    description = request.form.get("description")
    estimatedcost = request.form.get("estimatedcost")
    deadline = request.form.get("deadline")

    c.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?)",(orderid, clientid, str(orderdate), productname, description, estimatedcost, str(deadline))) 

    conn.commit()
    conn.close()
    return redirect('/editorders')

@app.route('/vieworders')
def render_all_orders():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    orders_query = c.execute("""SELECT * FROM orders""").fetchall()

    return render_template("orders.html", orders=orders_query)

@app.route('/editorders')
def render_editorders():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    orders_query = c.execute("""SELECT * FROM orders""").fetchall()

    return render_template("editorders.html", orders=orders_query)

@app.route('/editorders/<int:orderid>')
def editorder(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    post = c.execute("SELECT * FROM orders WHERE orderid=?", (orderid, )).fetchone() 
    #   print(post)
    return render_template('updateorder.html', posts=post)

@app.route('/updateorder/<int:orderid>', methods=["POST"])
def updateorder(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    # if request.method == "POST":
    orderid = request.form.get("orderid")
    clientid = request.form.get("clientid")
    orderdate = request.form.get("orderdate")
    productname = request.form.get("productname")
    description = request.form.get("description")
    estimatedcost = request.form.get("estimatedcost")
    deadline = request.form.get("deadline")

    t = (orderid,clientid,orderdate,productname,description,estimatedcost,deadline,orderid)
    # print(orderid,clientid)       
    c.execute("""UPDATE orders 
                     SET 
                     orderid=?,
                     clientid=?,
                     orderdate=?,
                     productname=?,
                     description=?,
                     estimatedcost=?,
                     deadline=?
                     WHERE orderid=?""", t)
    conn.commit()
    conn.close()

    return redirect('/editorders')
# return redirect('/')

@app.route('/deleteorder/<int:orderid>', methods=['POST', 'GET'])
def deleteorder(orderid):
        conn = sqlite3.connect('file.db')
        c = conn.cursor()

        c.execute("""DELETE FROM orders WHERE orderid = (?);""", (orderid,))

        conn.commit()
        conn.close()

        return redirect('/editorders')
# ``````````````````````````````````````````````````````````````````````````````````````````````````````

# ````````````````````````````RAWMATERIAL``````````````````````````````````````````
@app.route('/addrawmaterial')
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
    print(materials)


    c.execute("INSERT INTO rawmaterials VALUES (?, ?, ?, ?)",(clientid, orderid, materials, cost))
    conn.commit()
    conn.close()
    
    return redirect('/editrawmaterials')

# @app.route('/viewrawmaterials')
# def render_all_rawmaterials():
#     with sqlite3.connect('file.db') as conn:
#         c = conn.cursor()

#         rawmaterials_query = c.execute("""SELECT * FROM rawmaterials""").fetchall()

#         return render_template("rawmaterials.html", rawmaterials=rawmaterials_query)

@app.route('/editrawmaterials')
def render_editrawmaterials():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    rawmaterials_query = c.execute("""SELECT * FROM rawmaterials""").fetchall()

    return render_template("editrawmaterials.html", rawmaterials=rawmaterials_query)

@app.route('/editrawmaterials/<int:orderid>')
def editrawmaterial(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    post = c.execute("SELECT * FROM rawmaterials WHERE orderid=?", (orderid, )).fetchone() 
    #   print(post)
    return render_template('updaterawmaterial.html', posts=post)

@app.route('/updaterawmaterial/<int:orderid>', methods=["POST"])
def updaterawmaterial(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    # if request.method == "POST":
    clientid = request.form.get("clientid")
    orderid = request.form.get("orderid")
    materials = request.form.get("materials")
    cost = request.form.get("cost")

    t = (clientid,orderid,materials,cost,orderid)
    # print(orderid,clientid)       
    c.execute("""UPDATE rawmaterials 
                     SET 
                     orderid=?,
                     clientid=?,
                     materials=?,
                     cost=?
                     WHERE orderid=?""", t)
    conn.commit()
    conn.close()

    return redirect('/editrawmaterials')
# return redirect('/')

@app.route('/deleterawmaterial/<int:orderid>', methods=['POST', 'GET'])
def deleterawmaterial(orderid):
        conn = sqlite3.connect('file.db')
        c = conn.cursor()

        c.execute("""DELETE FROM rawmaterials WHERE orderid = (?);""", (orderid,))

        conn.commit()
        conn.close()

        return redirect('/editrawmaterials')
# ``````````````````````````````````````````````````````````````````````````````````````




# `````````````````````````````````````````PRODUCTION```````````````````````````````````````````````````````````````
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
    
    return redirect('/editproductions')

@app.route('/viewproductions')
def render_all_productions():
    with sqlite3.connect('file.db') as conn:
        c = conn.cursor()

        productions_query = c.execute("""SELECT * FROM production""").fetchall()

        return render_template("productions.html", productions=productions_query)

@app.route('/editproductions')
def render_editproductions():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    productions_query = c.execute("""SELECT * FROM production""").fetchall()

    return render_template("editproductions.html", productions=productions_query)

@app.route('/editproductions/<int:orderid>')
def editproduction(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    post = c.execute("SELECT * FROM production WHERE orderid=?", (orderid, )).fetchone() 
    #   print(post)
    return render_template('updateproduction.html', posts=post)

@app.route('/updateproduction/<int:orderid>', methods=["POST"])
def updateproduction(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    # if request.method == "POST":
    clientid = request.form.get("clientid")
    orderid = request.form.get("orderid")
    requireddays = request.form.get("requireddays")
    startdate = request.form.get("startdate")
    enddate = request.form.get("enddate")
    extradays = request.form.get("extradays")

    t = (clientid,orderid,requireddays,startdate,enddate, extradays, orderid)
    # print(orderid,clientid)       
    c.execute("""UPDATE production 
                     SET 
                     clientid=?,
                     orderid=?,
                     requireddays=?,
                     startdate=?,
                     enddate=?,
                     extradays=?
                     WHERE orderid=?""", t)
    conn.commit()
    conn.close()

    return redirect('/editproductions')
# return redirect('/')

@app.route('/deleteproduction/<int:orderid>', methods=['POST', 'GET'])
def deleteproduction(orderid):
        conn = sqlite3.connect('file.db')
        c = conn.cursor()

        c.execute("""DELETE FROM production WHERE orderid = (?);""", (orderid,))

        conn.commit()
        conn.close()

        return redirect('/editproductions')


# ``````````````````````````````````````````````````````````````````````````````````````````````````````

# ```````````````````````````````````````````SHIPMENT```````````````````````````````````````````````````````````
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
    
    c.execute("INSERT INTO shipment VALUES (?, ?, ?, ?, ?)",(clientid, orderid, weight, shippingaddress, transportationtype))
    conn.commit()
    conn.close()
    
    return redirect('/editshipments')

@app.route('/viewshipments')
def render_all_shipments():
    with sqlite3.connect('file.db') as conn:
        c = conn.cursor()

        shipments_query = c.execute("""SELECT * FROM shipment""").fetchall()

        return render_template("shipments.html", shipments=shipments_query)

@app.route('/editshipments')
def render_editshipments():
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    shipments_query = c.execute("""SELECT * FROM shipment""").fetchall()

    return render_template("editshipment.html", shipments=shipments_query)

@app.route('/editshipments/<int:orderid>')
def editshipment(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()

    post = c.execute("SELECT * FROM shipment WHERE orderid=?", (orderid, )).fetchone() 
    #   print(post)
    return render_template('updateshipment.html', posts=post)

@app.route('/updateshipment/<int:orderid>', methods=["POST"])
def updateshipment(orderid):
    conn = sqlite3.connect('file.db')
    c = conn.cursor()
    # if request.method == "POST":
    clientid = request.form.get("clientid")
    orderid = request.form.get("orderid")
    weight = request.form.get("weight")
    shipping_address = request.form.get("shipping_address")
    transportation_type = request.form.get("transportation_type")

    t = (orderid,clientid,weight,shipping_address, transportation_type, orderid)
    # print(orderid,clientid)       
    c.execute("""UPDATE shipment 
                     SET 
                     orderid=?,
                     clientid=?,
                     weight=?,
                     shipping_address=?,
                     transportation_type=?
                     WHERE orderid=?""", t)
    conn.commit()
    conn.close()

    return redirect('/editshipments')
# return redirect('/')

@app.route('/deleteshipments/<int:orderid>', methods=['POST', 'GET'])
def deleteshipment(orderid):
        conn = sqlite3.connect('file.db')
        c = conn.cursor()

        c.execute("""DELETE FROM shipment WHERE orderid = (?);""", (orderid,))

        conn.commit()
        conn.close()

        return redirect('/editshipments')


# ``````````````````````````````````````````````````````````````````````````````````````````````````````
