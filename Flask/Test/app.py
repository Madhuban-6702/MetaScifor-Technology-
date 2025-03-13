from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site1.db'  # SQLite DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'  # For sessions

db = SQLAlchemy(app)

# Product model (pre-filled with sample products)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(100), nullable=False)

# Initialize the database and create tables
with app.app_context():
    db.create_all()
    
    # Add products to the database if not already present (first time app setup)
    if not Product.query.first():
        products = [
            Product(name="Product 1", description="This is product 1", price=19.99, image_url="https://via.placeholder.com/200"),
            Product(name="Product 2", description="This is product 2", price=29.99, image_url="https://via.placeholder.com/200"),
            Product(name="Product 3", description="This is product 3", price=39.99, image_url="https://via.placeholder.com/200"),
        ]
        db.session.add_all(products)
        db.session.commit()

# Route for the landing page
@app.route('/')
def index():
    return render_template('index.html')

# Route to view all products
@app.route('/products')
def product_page():
    products = Product.query.all()
    return render_template('product_page.html', products=products)

# Add to cart route
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity_str = request.form.get('quantity', '1')  # Default to '1' if no input
    try:
        quantity = int(quantity_str)
    except ValueError:
        quantity = 1  # Set a default value if conversion fails

    cart = session.get('cart', {})
    
    if product.id in cart:
        cart[product.id]['quantity'] += quantity
    else:
        cart[product.id] = {
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'image_url': product.image_url
        }
    
    session['cart'] = cart
    return redirect(url_for('cart'))

# Cart page route
@app.route('/cart')
def cart():
    cart = session.get('cart', {})
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('cart.html', cart=cart, total_price=total_price)

# Checkout route
@app.route('/checkout')
def checkout():
    cart = session.get('cart', {})
    if not cart:
        return redirect(url_for('index'))
    
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('checkout.html', cart=cart, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
