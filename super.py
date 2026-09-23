import sqlite3

# ---------------- DATABASE ----------------

db = sqlite3.connect("supermarket.db")
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS products(
    name TEXT PRIMARY KEY,
    price REAL,
    stock INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS khata(
    customer TEXT PRIMARY KEY,
    amount REAL
)
""")

db.commit()


# ---------------- INVENTORY ----------------

def add_product(name, price, stock):
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
    print(f"✅ {name} added successfully.")


def show_inventory():
    cur.execute("SELECT * FROM products")
    products = cur.fetchall()

    print("\n📦 INVENTORY")
    print("-" * 35)

    if not products:
        print("No products available.")
        return

    for name, price, stock in products:
        print(f"{name} | ₹{price} | Stock: {stock}")


# ---------------- BILLING ----------------

def create_bill():
    total = 0
    bill_items = []

    while True:
        name = input("\nEnter product name (done to finish): ").lower()

        if name == "done":
            break

        cur.execute(
            "SELECT price, stock FROM products WHERE name=?",
            (name,)
        )

        product = cur.fetchone()

        if not product:
            print("❌ Product not found.")
            continue

        price, stock = product

        quantity = int(input("Enter quantity: "))

        if quantity > stock:
            print("❌ Not enough stock.")
            continue

        amount = price * quantity
        total += amount

        bill_items.append((name, quantity, price, amount))

        cur.execute("""
        UPDATE products
        SET stock=stock-?
        WHERE name=?
        """, (quantity, name))

    db.commit()

    print("\n🧾 BILL")
    print("-" * 40)

    for name, qty, price, amount in bill_items:
        print(f"{name} x {qty} = ₹{amount}")

    print("-" * 40)
    print(f"TOTAL = ₹{total}")


# ---------------- KHATA ----------------

def add_khata():
    customer = input("Customer name: ").lower()
    amount = float(input("Amount: "))

    cur.execute("SELECT amount FROM khata WHERE customer=?", (customer,))
    result = cur.fetchone()

    if result:
        new_amount = result[0] + amount

        cur.execute("""
        UPDATE khata
        SET amount=?
        WHERE customer=?
        """, (new_amount, customer))
    else:
        cur.execute("""
        INSERT INTO khata(customer, amount)
        VALUES (?, ?)
        """, (customer, amount))

    db.commit()

    print(f"✅ ₹{amount} added to {customer}'s Khata.")


def show_khata():
    cur.execute("SELECT * FROM khata")
    customers = cur.fetchall()

    print("\n📒 KHATA")
    print("-" * 30)

    for customer, amount in customers:
        print(f"{customer} : ₹{amount}")


# ---------------- SIMPLE AI AGENT ----------------

def agent(command):

    command = command.lower()

    if "inventory" in command or "stock" in command:
        show_inventory()

    elif "bill" in command:
        create_bill()

    elif "khata" in command:
        if "add" in command:
            add_khata()
        else:
            show_khata()

    elif "add product" in command:
        name = input("Product name: ").lower()
        price = float(input("Price: "))
        stock = int(input("Stock: "))

        add_product(name, price, stock)

    else:
        print("""
🤖 I don't understand that command.

Try:
1. Add product
2. Show inventory
3. Create bill
4. Add Khata
5. Show Khata
6. Exit
""")


# ---------------- MAIN PROGRAM ----------------

print("===================================")
print(" 🤖 SUPERMARKET OPS AGENT")
print("===================================")

while True:

    print("""
1. Add Product
2. Show Inventory
3. Create Bill
4. Add Khata
5. Show Khata
6. Exit
""")

    command = input("You: ")

    if command == "1":
        agent("add product")

    elif command == "2":
        agent("show inventory")

    elif command == "3":
        agent("create bill")

    elif command == "4":
        agent("add khata")

    elif command == "5":
        agent("show khata")

    elif command == "6":
        print("👋 Agent stopped.")
        break

    else:
        agent(command)

db.close()
