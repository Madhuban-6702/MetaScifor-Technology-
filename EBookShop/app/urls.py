from django.urls import path
from .views import home, register, login, logout_view, book_detail, add_to_cart, remove_from_cart, update_quantity, cart, profile, edit_profile, checkout, order_success

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name="register"),
    path('login/', login, name="login"),
    path('logout/', logout_view, name="logout"),
    path("cart/", cart, name="cart"), 
    path("book/<int:book_id>/", book_detail, name="book_detail"),
    path("add-to-cart/<int:book_id>/", add_to_cart, name="add_to_cart"),
    path('remove-from-cart/<int:book_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/update/<int:book_id>/', update_quantity, name='update_quantity'),
    path('profile/', profile, name='profile'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('checkout/', checkout, name='checkout'),
    path("order-success/", order_success, name="order_success"),
]
