from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite DB for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'mysecretkey'  # For session management

db = SQLAlchemy(app)

# Product model
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(100), nullable=False)

# Initialize the database and create tables
with app.app_context():
    db.create_all()
    
    # Add products to the database if not already present
    if not Product.query.first():
        products = [
            Product(name="Wireless Headphones", description="High-quality wireless headphones with noise-cancellation.", price=119.99, image_url="https://via.placeholder.com/200"),
            Product(name="Smart Watch", description="A sleek smartwatch with fitness tracking and notifications.", price=199.99, image_url="https://via.placeholder.com/200"),
            Product(name="Laptop Sleeve", description="Protect your laptop with this durable, padded laptop sleeve.", price=29.99, image_url="https://via.placeholder.com/200"),
        ]
        db.session.add_all(products)
        db.session.commit()

# Home route
@app.route('/')
def index():
    return render_template('index.html')

# Product page route
@app.route('/products')
def product_page():
    products = Product.query.all()
    return render_template('product_page.html', products=products)

# Add to cart route
@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))  # Default to 1 if not provided
    
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

# Remove from cart route
@app.route('/remove_from_cart/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    
    if product_id in cart:
        del cart[product_id]  # Remove the product from the cart
    
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
        return redirect(url_for('index'))  # Redirect to index if cart is empty
    
    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    return render_template('checkout.html', cart=cart, total_price=total_price)

if __name__ == '__main__':
    app.run(debug=True)
