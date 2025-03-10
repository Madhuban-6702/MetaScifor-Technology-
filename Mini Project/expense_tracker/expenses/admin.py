from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Expense, Income

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'phone')  # Add all fields you want to display
    list_filter = ('is_staff', 'is_active')  # You can add more filters if needed
    search_fields = ('username', 'email')  # Fields to search by
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user', 'source', 'amount', 'date')
    list_filter = ('user', 'date')
    search_fields = ('user__email', 'source')

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'amount', 'date')
    list_filter = ('user', 'category', 'date')
    search_fields = ('user__email', 'category')
    
admin.site.register(User, CustomUserAdmin)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Expense, ExpenseAdmin)
