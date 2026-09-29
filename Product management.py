import json
from datetime import datetime

pf = "products.json"
cf = "customers.json"
sf = "sales.json"

def ld(f):
    try:
        with open(f, "r") as x:
            return json.load(x)
    except:
        return {}

def sv(f, d):
    with open(f, "w") as x:
        json.dump(d, x, indent=4)

p = ld(pf)
c = ld(cf)
s = ld(sf)

def addp():
    n = input("Product name: ")
    q = int(input("Stock quantity: "))
    cp = float(input("Cost price: "))
    sp = float(input("Selling price: "))

    p[n] = {
        "stock": q,
        "sold": 0,
        "cost": cp,
        "price": sp
    }

    sv(pf, p)
    print("Product added")

def showp():
    if not p:
        print("No products found")
        return

    print("\nProduct Details")
    print("-" * 60)

    for n, v in p.items():
        print("Name:", n)
        print("Stock:", v["stock"])
        print("Sold:", v["sold"])
        print("Cost:", v["cost"])
        print("Price:", v["price"])
        print()

def sellp():
    n = input("Product name: ")

    if n not in p:
        print("Product not found")
        return

    q = int(input("Quantity sold: "))

    if q > p[n]["stock"]:
        print("Not enough stock")
        return

    cn = input("Customer name: ")
    ph = input("Customer phone: ")
    pm = float(input("Payment received: "))

    cp = p[n]["cost"]
    sp = p[n]["price"]

    sub = sp * q
    gst = sub * 0.18
    tot = sub + gst
    cost = cp * q
    pro = sub - cost
    due = tot - pm

    p[n]["stock"] -= q
    p[n]["sold"] += q

    dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    sn = str(len(s) + 1)

    s[sn] = {
        "product": n,
        "quantity": q,
        "customer": cn,
        "phone": ph,
        "cost": cost,
        "sale": sub,
        "gst": gst,
        "total": tot,
        "paid": pm,
        "due": due,
        "profit": pro,
        "date": dt
    }

    if ph not in c:
        c[ph] = {
            "name": cn,
            "phone": ph,
            "due": 0,
            "date": dt
        }

    c[ph]["due"] += due

    sv(pf, p)
    sv(cf, c)
    sv(sf, s)

    print("\nSale completed")
    print("Subtotal:", round(sub, 2))
    print("GST 18%:", round(gst, 2))
    print("Total:", round(tot, 2))
    print("Paid:", round(pm, 2))
    print("Due:", round(due, 2))
    print("Profit:", round(pro, 2))

def shows():
    if not s:
        print("No sales found")
        return

    print("\nSales Details")
    print("-" * 70)

    for n, v in s.items():
        print("Sale:", n)
        print("Product:", v["product"])
        print("Quantity:", v["quantity"])
        print("Customer:", v["customer"])
        print("Total:", round(v["total"], 2))
        print("Paid:", round(v["paid"], 2))
        print("Due:", round(v["due"], 2))
        print("Profit:", round(v["profit"], 2))
        print("Date:", v["date"])
        print()

def showc():
    if not c:
        print("No customers found")
        return

    print("\nCustomer Due Payments")
    print("-" * 60)

    for n, v in c.items():
        print("Name:", v["name"])
        print("Phone:", v["phone"])
        print("Due:", round(v["due"], 2))
        print("Date:", v["date"])
        print()

def pay():
    ph = input("Customer phone: ")

    if ph not in c:
        print("Customer not found")
        return

    d = c[ph]["due"]

    if d <= 0:
        print("No due payment")
        return

    print("Current due:", round(d, 2))

    x = float(input("Payment amount: "))

    if x > d:
        print("Payment is greater than due")
        return

    c[ph]["due"] -= x

    dt = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    c[ph]["date"] = dt

    sv(cf, c)

    print("Payment updated")
    print("Remaining due:", round(c[ph]["due"], 2))

def rep():
    ts = 0
    tc = 0
    tg = 0
    tp = 0
    td = 0

    for v in s.values():
        ts += v["total"]
        tc += v["cost"]
        tg += v["gst"]
        tp += v["profit"]
        td += v["due"]

    print("\nBusiness Report")
    print("-" * 50)
    print("Total sales:", round(ts, 2))
    print("Total cost:", round(tc, 2))
    print("Total GST:", round(tg, 2))
    print("Total profit:", round(tp, 2))
    print("Total due:", round(td, 2))

def menu():
    while True:
        print("\nPRODUCT MANAGEMENT SYSTEM")
        print("1. Add Product")
        print("2. Show Products")
        print("3. Sell Product")
        print("4. Show Sales")
        print("5. Show Customers")
        print("6. Receive Due Payment")
        print("7. Business Report")
        print("8. Exit")

        x = input("Enter choice: ")

        if x == "1":
            addp()
        elif x == "2":
            showp()
        elif x == "3":
            sellp()
        elif x == "4":
            shows()
        elif x == "5":
            showc()
        elif x == "6":
            pay()
        elif x == "7":
            rep()
        elif x == "8":
            print("Thank you")
            break
        else:
            print("Invalid choice")

menu()