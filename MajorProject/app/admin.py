from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import reverse, path
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from .models import CustomUser, Trek, Booking, Discount
from django.shortcuts import render, redirect
import logging

logger = logging.getLogger(__name__)

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'email', 'phone_number', 'is_staff', 'is_active')  # Fields shown in the admin list view
    search_fields = ('username', 'email', 'phone_number')  # Enable search by username, email, and phone
    list_filter = ('is_staff', 'is_active')  # Filters for active/staff users

# Register the CustomUser model with the customized admin view
admin.site.register(CustomUser, CustomUserAdmin)

class TrekAdmin(admin.ModelAdmin):
    list_display = ('trek_id', 'name', 'difficulty', 'season', 'duration', 'price', 
                    'pickup_location', 'drop_location', 'meals', 'image', 'description')  # Display all fields
    search_fields = ('name', 'difficulty', 'season', 'pickup_location', 'drop_location')  # Allow searching by multiple fields
    list_filter = ('difficulty', 'season', 'duration')  # Filters for sidebar
    ordering = ('name',)  # Order by trek name
    readonly_fields = ('image',)  # Prevent accidental image changes

admin.site.register(Trek, TrekAdmin)

from .models import Booking  # Import the Booking model

class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'date', 'trek', 'number_of_people', 'total_price')  # ✅ Show trek details
    search_fields = ('name', 'email', 'trek__name')  # ✅ Allow searching by trek name
    list_filter = ('date', 'trek')  # ✅ Add filtering by trek

admin.site.register(Booking, BookingAdmin)

admin.site.site_header = "         _   "
# admin.site.site_title = "Sahyadri Admin"
# admin.site.index_title = "Welcome to Sahyadri Trails Admin"

class CustomAdminSite(admin.AdminSite):
    site_header = "Travel Admin Panel"
    site_title = "Admin Dashboard"
    index_title = "Welcome to the Travel Admin Panel"

    def login(self, request, extra_context=None):
        response = super().login(request, extra_context)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('admin_dashboard'))  # Redirect to custom dashboard
        return response

admin_site = CustomAdminSite(name='custom_admin')



class DiscountAdmin(admin.ModelAdmin):
    list_display = ('title', 'percentage', 'start_date', 'end_date', 'created_at', 'send_notification_button')
    list_filter = ('start_date', 'end_date')
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('send-discount/<int:discount_id>/', self.admin_site.admin_view(self.send_discount), name='send_discount'),
        ]
        return custom_urls + urls  # Append to admin URLs

    def send_discount(self, request, discount_id):
        try:
            discount = Discount.objects.get(id=discount_id)
            bookings = Booking.objects.values_list('email', flat=True).distinct()
            recipient_list = list(bookings)  # Convert to list

            if recipient_list:
                subject = f"🎉 Exclusive Discount: {discount.title}"
                html_content = render_to_string("admin/discount_email.html", {"discount": discount})
                text_content = strip_tags(html_content)

                email = EmailMultiAlternatives(
                    subject=subject,
                    body=text_content,
                    from_email="yourcompany@example.com",
                    to=recipient_list,
                )
                email.attach_alternative(html_content, "text/html")  
                email.send(fail_silently=False)

                messages.success(request, f"Discount notification sent to {len(recipient_list)} users!")
                logger.info(f"Discount email sent to {recipient_list}")
            else:
                messages.warning(request, "No users found with a registered email!")

        except Discount.DoesNotExist:
            messages.error(request, "Discount not found!")
            logger.error("Discount not found!")

        return redirect('/admin/app/discount/')

    def send_notification_button(self, obj):
        url = reverse("admin:send_discount", args=[obj.id])
        return mark_safe(f'<a href="{url}" class="button" style="background-color: green; padding: 5px 10px; color: white; text-decoration: none; border-radius: 5px;">Send Notification</a>')

    send_notification_button.short_description = "Notify Users"

admin.site.register(Discount, DiscountAdmin)
