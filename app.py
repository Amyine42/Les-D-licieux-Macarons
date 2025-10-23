from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "macaron_secret_key"

# --- Configuration PostgreSQL (RDS) ---
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL",
    "sqlite:///macarons.db"  # fallback local (utile en test)
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --- Modèle de table ---
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    address = db.Column(db.Text)
    items = db.Column(db.Text)
    total = db.Column(db.Float)

# --- Données macarons ---
MACARONS = [
    {"id": 1, "name": "Pistachio", "price": 2.5, "image": "pistachio.jpg"},
    {"id": 2, "name": "Chocolate", "price": 2.8, "image": "chocolate.jpg"},
    {"id": 3, "name": "Raspberry", "price": 2.6, "image": "raspberry.jpg"},
]

# ✅ Crée les tables au démarrage
with app.app_context():
    db.create_all()

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html", macarons=MACARONS)

@app.route("/add_to_cart/<int:macaron_id>")
def add_to_cart(macaron_id):
    macaron = next((m for m in MACARONS if m["id"] == macaron_id), None)
    if macaron:
        cart = session.get("cart", [])
        cart.append(macaron)
        session["cart"] = cart
    return redirect(url_for("home"))

@app.route("/cart")
def cart_page():
    cart = session.get("cart", [])
    total = sum(m["price"] for m in cart)
    return render_template("cart.html", cart=cart, total=total)

@app.route("/order", methods=["GET", "POST"])
def order_page():
    if request.method == "POST":
        name = request.form["name"]
        address = request.form["address"]
        cart = session.get("cart", [])
        total = sum(m["price"] for m in cart)

        # Sauvegarde en base
        order = Order(
            customer_name=name,
            address=address,
            items=str(cart),
            total=total
        )
        db.session.add(order)
        db.session.commit()

        # Vide le panier
        session["cart"] = []

        # Retour à la page order.html avec succès
        return render_template("order.html", success=True, name=name, total=total)

    return render_template("order.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)