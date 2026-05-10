from flask import Flask, render_template, request, redirect, session
from flower_database import Inventory, Flower, Order, Customer, Payment

app = Flask(__name__)
app.secret_key = "flower_secret"

inv = Inventory()


# ---------------- HOME ----------------
@app.route("/")
def home():
    flowers = inv.show_inventory()
    total = session.get("total", 0)
    return render_template("index.html", flowers=flowers, total=total)


# ---------------- ADD FLOWER ----------------
@app.route("/add", methods=["POST"])
def add_flower():
    name = request.form["name"]
    price = float(request.form["price"])
    qty = int(request.form["qty"])

    inv.add_flower(Flower(name, price, qty))
    return redirect("/")


# ---------------- ORDER ----------------
@app.route("/order", methods=["POST"])
def order():
    name = request.form["flower_name"]
    qty = int(request.form["qty"])
    customer = request.form["customer"]

    order = Order(inv)
    order.add_items(name, qty, customer)

    total = order.checkout()
    session["total"] = total
    session["customer"] = customer

    return redirect("/")


# ---------------- CHECKOUT (NEW) ----------------
@app.route("/checkout")
def checkout():
    total = session.get("total", 0)
    customer = session.get("customer", "Guest")

    payment = Payment(total)
    message = payment.process_payment()

    # reset cart after checkout
    session["total"] = 0

    return render_template("checkout.html", total=total, customer=customer, message=message)


# ---------------- CLEAR ----------------
@app.route("/clear")
def clear():
    session["total"] = 0
    session["customer"] = ""
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
