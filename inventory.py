from database import get_connection

def add_product(name, price, stock):
    db = get_connection()
    cur = db.cursor()

    cur.execute("SELECT * FROM products WHERE name=?", (name,))
    product = cur.fetchone()

    if product:
        cur.execute("""
        UPDATE products
        SET price=?, stock=stock+?
        WHERE name=?
        """, (price, stock, name))
    else:
        cur.execute("""
        INSERT INTO products(name, price, stock)
        VALUES (?, ?, ?)
        """, (name, price, stock))

    db.commit()
    db.close()

    print("Product added successfully.")


def show_inventory():
    db = get_connection()
    cur = db.cursor()

    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    print("\n--- INVENTORY ---")

    for product in products:
        print(
            f"Name: {product[0]} | "
            f"Price: ₹{product[1]} | "
            f"Stock: {product[2]}"
        )

    db.close()
