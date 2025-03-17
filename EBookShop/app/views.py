from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from .models import User, Book, Order, OrderItem
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    query = request.GET.get("q", "")  # Get search query from URL
    books = Book.objects.filter(title__icontains=query) if query else Book.objects.all()  # Search if query exists
    
    paginator = Paginator(books, 8)  # Show 8 books per page
    page_number = request.GET.get("page")  # Get current page number
    page_books = paginator.get_page(page_number)  # Get books for the page

    last_order = None
    if request.user.is_authenticated:  # Ensure user is logged in
        last_order = Order.objects.filter(user=request.user).last()  # Get last order for user

    return render(request, "home.html", {"books": page_books, "query": query, "last_order": last_order})

# Registration View
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        address = request.POST['address']
        password = request.POST['password']

        if User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            messages.error(request, "Username or email already exists")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password, full_name=full_name, phone=phone, address=address)
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')

    return render(request, 'register.html')

# Login View
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = User.objects.filter(username=username).first()

        if user:
            user = authenticate(request, email=user.email, password=password)  # Authenticate with email
            if user is not None:
                auth_login(request, user)
                messages.success(request, "Login successful!")
                return redirect('home')
        
        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'login.html')

# Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_detail.html", {
        "book": book,
        "genres_list": book.category_name.split(", "),  # Assuming categories are stored as comma-separated values
    })


def cart(request):
    cart = request.session.get('cart', {})
    
    for book_id, book in cart.items():
        book['total_price'] = book['quantity'] * book['price']  # Calculate total price
    
    request.session['cart'] = cart  # Update session

    return render(request, 'cart.html', {'cart': cart})

def add_to_cart(request, book_id):
    """ Add a book to the cart with dynamic quantity """
    if not request.user.is_authenticated:
        messages.info(request, "You need to log in to add items to the cart.")
        return redirect(f"{reverse('login')}?next={request.path}")

    book = get_object_or_404(Book, id=book_id)
    cart = request.session.get('cart', {})

    # Get the selected quantity from the form submission (default to 1)
    selected_quantity = int(request.POST.get('quantity', 1))

    if str(book_id) in cart:
        # Update quantity to the selected value instead of incrementing
        cart[str(book_id)]['quantity'] = selected_quantity
    else:
        cart[str(book_id)] = {
            'title': book.title,
            'price': float(book.price),  # Ensure JSON serializable
            'quantity': selected_quantity,
            'imgUrl': book.imgUrl
        }

    request.session['cart'] = cart
    messages.success(request, f"Added {selected_quantity} of {book.title} to cart.")
    return redirect(reverse('cart'))

def remove_from_cart(request, book_id):
    """ Remove a book from the cart """
    cart = request.session.get('cart', {})

    if str(book_id) in cart:
        del cart[str(book_id)]
        request.session['cart'] = cart
        messages.success(request, "Book removed from cart.")
    else:
        messages.error(request, "Book not found in cart.")

    return redirect(reverse('cart'))


def update_quantity(request, book_id):
    """ Increase or decrease item quantity in cart """
    cart = request.session.get('cart', {})

    if str(book_id) in cart:
        action = request.POST.get('action')

        if action == 'increase':
            cart[str(book_id)]['quantity'] += 1
        elif action == 'decrease' and cart[str(book_id)]['quantity'] > 1:
            cart[str(book_id)]['quantity'] -= 1

        request.session['cart'] = cart
        messages.success(request, f"Updated quantity for {cart[str(book_id)]['title']}.")

    return redirect(reverse('cart'))

@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST['username']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        address = request.POST['address']

        # Check if the new username already exists (excluding the current user)
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, "Username is already taken. Please choose another.")
            return redirect('profile')

        # Check if the new email already exists (excluding the current user)
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, "Email is already registered. Please use another.")
            return redirect('profile')

        # Split full_name into first_name and last_name safely
        name_parts = full_name.strip().split(" ", 1)
        first_name = name_parts[0]
        last_name = name_parts[1] if len(name_parts) > 1 else ""

        # Update user details
        user.username = username
        user.first_name = first_name  # Correctly update first_name
        user.last_name = last_name  # Correctly update last_name
        user.email = email
        user.phone = phone_number  # Ensure your CustomUser model has a `phone` field
        user.address = address  # Ensure your CustomUser model has an `address` field

        try:
            user.save()
            messages.success(request, "Profile updated successfully!")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect('profile')

    return render(request, 'profile.html')

@login_required
def checkout(request):
    """ Checkout process: Review cart and place an order """
    cart = request.session.get('cart', {})

    if not cart:
        messages.warning(request, "Your cart is empty!")
        return redirect('cart')

    if request.method == "POST":
        # Calculate estimated delivery date
        date_of_delivery = timezone.localtime(timezone.now()) + timedelta(days=7)

        # Create the order
        order = Order.objects.create(user=request.user, date_of_delivery=date_of_delivery)

        # Create order items
        for book_id, item in cart.items():
            book = Book.objects.get(id=book_id)
            OrderItem.objects.create(
                order=order,
                book=book,
                quantity=item['quantity'],
                price=item['price']
            )

        # Clear the cart after the order is placed
        request.session['cart'] = {}

        messages.success(request, "Order placed successfully!")
        return redirect('order_success')

    return render(request, 'checkout.html', {'cart': cart})

@login_required
def order_success(request):
    """ Order success page with full order details """
    try:
        order = Order.objects.filter(user=request.user).latest('date_placed')  # Check latest order
        order_items = OrderItem.objects.filter(order=order)
    except Order.DoesNotExist:
        order = None  # If no order exists
        order_items = None

    if not order:
        return render(request, 'no_order.html')  # If no order exists, show 'no_order' template

    context = {
        'order': order,
        'order_items': order_items,  # Pass order items to template
        'date_of_delivery': order.date_of_delivery,  # Fetch from order
        'user': request.user,  # Pass user details
    }

    return render(request, 'order_success.html', context)