from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "macaron_secret_key"

# Sample macaron data
MACARONS = [
    {"id": 1, "name": "Pistachio", "price": 2.5, "image": "pistachio.jpg"},
    {"id": 2, "name": "Chocolate", "price": 2.8, "image": "chocolate.jpg"},
    {"id": 3, "name": "Raspberry", "price": 2.6, "image": "raspberry.jpg"}
]

@app.route('/')
def index():
    return render_template('index.html', macarons=MACARONS)

@app.route('/add_to_cart/<int:macaron_id>')
def add_to_cart(macaron_id):
    macaron = next((m for m in MACARONS if m["id"] == macaron_id), None)
    if macaron:
        cart = session.get('cart', [])
        cart.append(macaron)
        session['cart'] = cart
    return redirect(url_for('index'))

@app.route('/cart')
def cart():
    cart = session.get('cart', [])
    total = sum(item["price"] for item in cart)
    return render_template('cart.html', cart=cart, total=total)

@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        name = request.form['name']
        address = request.form['address']
        cart = session.get('cart', [])
        total = sum(item["price"] for item in cart)
        session.pop('cart', None)
        return render_template('order.html', name=name, address=address, total=total)
    return redirect(url_for('cart'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
