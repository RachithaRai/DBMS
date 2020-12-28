import sqlite3

def init_db():
    with sqlite3.connect("file.db") as conn:
        c = conn.cursor()

        # c.execute("DROP TABLE orders")
        # conn.commit()

        c.execute("""   CREATE TABLE IF NOT EXISTS client (
                        clientid INTEGER PRIMARY KEY,
                        clientusername TEXT,
                        password TEXT,
                        company TEXT,
                        address TEXT,
                        name TEXT,
                        contact INTEGER,
                        mailid TEXT
                );
                """)
        conn.commit()

        conn.commit()


        c.execute("""   CREATE TABLE IF NOT EXISTS orders (
                        orderid INTEGER PRIMARY KEY,
                        clientid INTEGER,
                        orderdate TEXT,
                        productname TEXT,
                        description TEXT,
                        estimatedcost INTEGER,
                        deadline Text,
                        FOREIGN KEY(clientid) REFERENCES client(clientid) ON DELETE CASCADE
                );
                """)
        conn.commit()
        

        c.execute("""   CREATE TABLE IF NOT EXISTS rawmaterials (
                        clientid INTEGER,
                        orderid INTEGER,
                        materials TEXT,
                        cost REAL,
                        FOREIGN KEY(clientid) REFERENCES client(clientid) ON DELETE CASCADE,
                        FOREIGN KEY(orderid) REFERENCES orders(orderid) ON DELETE CASCADE
                );
                """)

        conn.commit()

        c.execute("""   CREATE TABLE IF NOT EXISTS production(
                        clientid INTEGER,
                        orderid INTEGER,
                        requireddays INTEGER,
                        startdate TEXT,
                        enddate TEXT,
                        extradays INTEGER,
                        FOREIGN KEY(orderid) REFERENCES orders(orderid) ON DELETE CASCADE,
                        FOREIGN KEY (clientid) REFERENCES client(clientid) ON DELETE CASCADE


                );
                """)
        conn.commit()

        c.execute("""   CREATE TABLE IF NOT EXISTS shipment(
                        clientid INTEGER,
                        orderid INTEGER,
                        weight REAL,
                        shipping_address TEXT,
                        transportation_type TEXT,
                        FOREIGN KEY (clientid) REFERENCES client(clientid) ON DELETE CASCADE,
                        FOREIGN KEY(orderid) REFERENCES orders(orderid) ON DELETE CASCADE

                );
                """)
        conn.commit()

init_db()