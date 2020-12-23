import sqlite3

def init_db():
    with sqlite3.connect("file.db") as conn:
        c = conn.cursor()

        # c.execute("DROP TABLE orders")
        # conn.commit()

        c.execute("""   CREATE TABLE IF NOT EXISTS customer (
                        customerid INTEGER PRIMARY KEY,
                        company TEXT,
                        address TEXT,
                        name TEXT,
                        contact INTEGER,
                        maild TEXT
                );
                """)
        conn.commit()
        c.execute("""   CREATE TABLE IF NOT EXISTS orders (
                        orderid INTEGER PRIMARY KEY,
                        customerid INTEGER,
                        orderdate TEXT,
                        productname TEXT,
                        productid INTEGER,
                        description TEXT,
                        estimatedcost INTEGER,
                        deadline Text,
                        FOREIGN KEY(customerid) REFERENCES customer(customerid) ON DELETE CASCADE
                );
                """)
        conn.commit()
        

        c.execute("""   CREATE TABLE IF NOT EXISTS rawmaterials (
                        customerid INTEGER,
                        orderid INTEGER,
                        materials TEXT,
                        cost REAL,
                        deliverydate TEXT,
                        isDelivered INTEGER,
                        FOREIGN(customerid) REFERENCES customer(customerid) ON DELETE CASCADE,
                        FOREIGN KEY(orderid) REFERENCES orders(orderid) ON DELETE CASCADE
                );
                """)

        conn.commit()

        c.execute("""  CREATE TABLE IF NOT EXISTS production(
                        customerid INTEGER,
                        orderid INTEGER,
                        requireddays INTEGER,
                        startdate TEXT,
                        enddate TEXT,
                        extradays INTEGER,
                        FOREIGN KEY(orderid) REFERENCES orders(orderid) ON DELETE CASCADE,
                        FOREIGN KEY (customerid) REFERENCES customer(customerid) ON DELETE CASCADE


                );
                """)
        conn.commit()

        c.execute("""   CREATE TABLE IF NOT EXISTS shipment(
                        customerid INTEGER,
                        orderid INTEGER,
                        weight REAL,
                        shipping_address TEXT,
                        transportation_type TEXT,
                        FOREIGN KEY (customerid) REFERENCES customer(customerid) ON DELETE CASCADE,
                        FOREIGN KEY(orderid) REFERENCES orders(orderid) ON DELETE CASCADE

                );
                """)
        conn.commit()

init_db()