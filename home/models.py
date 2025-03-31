from django.db import models
from django.contrib.auth.models import User  # For linking service providers to users
from authentication.models import Profile

# Service Provider Model
class ServiceProvider(models.Model):
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name="service_provider")
    business_name = models.CharField(max_length=255)
    category_choices = [
        ("Medical", "Medical"),
        ("Mechanical", "Mechanical"),
        ("Electrician", "Electrician"),
        ("Cleaning", "Cleaning"),
    ]
    category = models.CharField(max_length=20, choices=category_choices)
    contact_number = models.CharField(max_length=15)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to="providers/", null=True, blank=True)
    rating = models.FloatField(default=0.0)
    status = models.CharField(max_length=10, choices=[("Active", "Active"), ("Inactive", "Inactive"), ("Pending", "Pending")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.business_name

# Services Model
class Service(models.Model):
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="services")
    service_name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category_choices = [
        ("Medical", "Medical"),
        ("Mechanical", "Mechanical"),
        ("Electrician", "Electrician"),
        ("Cleaning", "Cleaning"),
    ]
    rating = models.FloatField(default=0.0)
    category = models.CharField(max_length=20, choices=category_choices)
    availability = models.BooleanField(default=True)
    service_image = models.ImageField(upload_to="services/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.service_name

# Booking Model
class Booking(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="bookings")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="bookings")
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateField()
    booking_time = models.TimeField()
    status_choices = [
        ("Pending", "Pending"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default="Pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_status = models.CharField(max_length=10, choices=[("Pending", "Pending"), ("Paid", "Paid"), ("Failed", "Failed")], default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.service.service_name}"

# Review Model
class Review(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="reviews")
    provider = models.ForeignKey(ServiceProvider, on_delete=models.CASCADE, related_name="reviews")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="reviews")
    rating = models.FloatField()
    review_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.user.username} - {self.rating}⭐"

# Payment Model
class Payment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="payments")
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name="payments")
    payment_method = models.CharField(max_length=20, choices=[("Credit Card", "Credit Card"), ("Debit Card", "Debit Card"), ("UPI", "UPI"), ("Net Banking", "Net Banking"), ("Cash", "Cash")])
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=10, choices=[("Success", "Success"), ("Failed", "Failed"), ("Pending", "Pending")], default="Pending")
    transaction_id = models.CharField(max_length=255, unique=True)
    payment_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.transaction_id} - {self.payment_status}"
