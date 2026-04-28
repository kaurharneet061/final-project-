import sqlite3

# Flower class
class Flower:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty


# Inventory class
class Inventory:
    def __init__(self):
        self.conn = sqlite3.connect("flowers-database.db")
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory (
            name TEXT PRIMARY KEY,
            price REAL,
            qty INTEGER
            )
        """)
        self.conn.commit()

    def add_flower(self, flower):
        self.cursor.execute(
            "INSERT OR REPLACE INTO inventory VALUES (?, ?, ?)",
            (flower.name, flower.price, flower.qty)
        )
        self.conn.commit()

    def show_inventory(self):
        self.cursor.execute("SELECT * FROM inventory")
        return self.cursor.fetchall()

    def get_flower(self, name):
        self.cursor.execute(
            "SELECT price, qty FROM inventory WHERE name = ?", (name,)
        )
        return self.cursor.fetchone()

    def update_stock(self, name, amount):
        self.cursor.execute(
            "UPDATE inventory SET qty = qty - ? WHERE name = ?",
            (amount, name)
        )
        self.conn.commit()

# Order class
class Order:
    def __init__(self, inventory):
        self.inventory = inventory
        self.items = []
    
    def add_items(self, name, qty):
        data = self.inventory.get_flower(name)

        if data:
            price, stock = data
            if qty <= stock:
                self.items.append((name, qty, price))
                self.inventory.update_stock(name, qty)
            else:
                print("Not enough stock")
        else:
            print("Flower not found")

    def checkout(self):
        total = 0
        for name, qty, price in self.items:
            total += qty * price
        return total
