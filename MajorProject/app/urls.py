from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout_view, name='logout_view'),
    path('profile/', views.profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('verify-otp/<uidb64>/', views.verify_otp, name='verify_otp'),  # OTP verification page
    path('resend-otp/<uidb64>/', views.resend_otp, name='resend_otp'), 
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_forgot_password_otp/', views.verify_forgot_password_otp, name='verify_otp'),
    path('resend_forgot_password_otp/', views.resend_forgot_password_otp, name='resend_forgot_password_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('explore/', views.explore_treks, name='explore_treks'),
    path('contact/', views.contact, name='contact'),
    path('bookings/', views.bookings_page, name='bookings_page'),
    path("create-booking/", views.create_booking, name="create_booking"),
    path('booking_details/', views.booking_details, name='booking_details'),
     path('download/<int:booking_id>/', views.download_booking_pdf, name='download_booking'),
     path("chat/", views.chatbot_response, name="chatbot_response"), 
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    # path('admin/send-discount/<int:discount_id>/',views.send_discount, name='send_discount'),
]
