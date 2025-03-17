from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)  # Store OTP
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

class Trek(models.Model):
    trek_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    difficulty = models.CharField(
        max_length=20,
        choices=[('easy', 'Easy'), ('moderate', 'Moderate'), ('hard', 'Hard')]
    )
    season = models.CharField(
        max_length=20,
        choices=[('monsoon', 'Monsoon'), ('winter', 'Winter'), ('summer', 'Summer')]
    )
    duration = models.CharField(
        max_length=20,
        choices=[('one-day', 'One-Day'), ('weekend', 'Weekend')]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='media/')
    description = models.TextField()
    pickup_location = models.CharField(max_length=255, default="Nearest Railway Station")
    drop_location = models.CharField(max_length=255, default="Lonavala Railway Station")
    meals = models.TextField(default="Breakfast, Lunch, Dinner included")

    def __str__(self):
        return self.name


    
class Booking(models.Model):
    trek = models.ForeignKey('Trek', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)  # Store user-entered name
    email = models.EmailField()  # Store user-entered email
    date = models.DateField()  # User-selected date
    number_of_people = models.PositiveIntegerField()  # User-selected number of people
    total_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)  # Auto-calculated

    def save(self, *args, **kwargs):
        """ Automatically calculate total price before saving """
        if self.trek:  # Ensure trek is assigned
            self.total_price = self.trek.price * self.number_of_people
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.name} - {self.date} ({self.number_of_people} people)"
    
    

class Discount(models.Model):
    title = models.CharField(max_length=200)  # Discount Title
    description = models.TextField()  # Discount Details
    percentage = models.FloatField()  # Discount Percentage
    start_date = models.DateTimeField(default=timezone.now)  # Discount Start Date
    end_date = models.DateTimeField()  # Discount End Date
    created_at = models.DateTimeField(auto_now_add=True)  # Date Created

    def is_active(self):
        """Check if the discount is currently active based on start and end dates."""
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    def __str__(self):
        return f"{self.title} - {self.percentage}% (Valid: {self.start_date.date()} to {self.end_date.date()})"
