from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Book, Order,OrderItem

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'full_name', 'email', 'phone', 'address', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'email', 'phone', 'address')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'full_name', 'email', 'phone', 'address', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

admin.site.register(User, CustomUserAdmin)
class OrderItemInline(admin.TabularInline):  # Display order items inline in order details
    model = OrderItem
    extra = 0
    fields = ['book', 'quantity', 'price']
    readonly_fields = ['book', 'quantity', 'price']

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'date_placed', 'date_of_delivery']  # Show key details in order list
    list_filter = ['date_placed', 'user']  # Filter by user
    search_fields = ['user__username', 'id']  # Enable search by username and order ID
    inlines = [OrderItemInline]  # Show order items inside the order details

    def get_queryset(self, request):
        """Show only orders belonging to the logged-in admin user (if non-superuser)."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see all orders
        return qs.filter(user=request.user)  # Regular users see only their orders

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'book', 'quantity', 'total_price']
    list_filter = ['order__user']
    search_fields = ['order__id', 'book__title']

    def get_queryset(self, request):
        """Show only order items belonging to the logged-in admin user."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(order__user=request.user)

# Register models with custom admin views
admin.site.register(Book)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
