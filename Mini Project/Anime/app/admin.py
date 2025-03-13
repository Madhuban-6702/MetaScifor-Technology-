from django.contrib import admin
from .models import *

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # Import your CustomUser model

# Customizing the Django Admin Panel for CustomUser
class CustomUserAdmin(UserAdmin):
    # Fields to be displayed in the admin panel list view
    list_display = ('username', 'full_name', 'email', 'is_active', 'is_staff', 'date_joined')
    
    # Fields to be clickable (edit page link)
    list_display_links = ('username', 'email')

    # Fields to filter users in the admin panel
    list_filter = ('is_active', 'is_staff')

    # Search functionality in admin panel
    search_fields = ('username', 'email', 'full_name')

    # Organizing the admin form layout
    fieldsets = (
        ("Personal Info", {"fields": ("username", "full_name", "email", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important Dates", {"fields": ("last_login", "date_joined")}),
    )

    # Fields displayed when adding a new user
    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": ("username", "full_name", "email", "password1", "password2"),
        }),
    )

# Register CustomUser with the CustomUserAdmin configuration
admin.site.register(CustomUser, CustomUserAdmin)

admin.site.register(Anime)

class WatchlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_animes')  # Show user and their anime list
    search_fields = ('user__username', 'animes__name')  # Search by username or anime name
    
    def display_animes(self, obj):
        """Display all animes added to the watchlist as a comma-separated string."""
        return ", ".join([anime.name for anime in obj.animes.all()])
    
    display_animes.short_description = "Animes in Watchlist"

    def get_queryset(self, request):
        """Filter watchlist to show only the logged-in user's watchlist unless the user is a superuser."""
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs  # Superusers see all watchlists
        return qs.filter(user=request.user)  # Regular users see only their own watchlist

admin.site.register(Watchlist, WatchlistAdmin)