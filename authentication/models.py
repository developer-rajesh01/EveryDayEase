from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from datetime import datetime

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('O', 'Other'),
)

# Create your models here.
class Profile(AbstractUser):
    USER_TYPES = (
        ('customer', 'Customer'),
        ('shopkeeper', 'Shopkeeper'),
        ('staff', 'Staff'),
        ('admin', 'Admin'),
    )

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True,default='./profile_images/user.png')
    city = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(max_length=500, blank=True, null=True)

    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='customer')
    update_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.username
    

# Feedback Model
class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='feedbacks')
    content = models.TextField(default="", help_text="Specify the associated content (e.g., product or post).",blank=True)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES, default=3)
    fid = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    real = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"Rating: {self.rating} by {self.user.username} for {self.content}"


class ContactServices(models.Model):
    name= models.CharField(max_length=50)
    email = models.EmailField(max_length=150)
    subject = models.CharField(max_length=30, choices=(('General Customer Service','General Customer'),('Suggestions','Suggestions'),('Product Suppport','Product Support')))
    message = models.TextField(default="", help_text="Mention your resion to contact us",blank=True,null=False)
    created_date = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f"{self.name} : {self.email}"
    

class ShopkeeperProfile(models.Model):

    service_type_list = [
        ('medical', 'Medical'),
        ('mechanical', 'Mechanical'),
        ('electrical', 'Electrical'),
        ('cleaning', 'Cleaning'),
        ('door-to-door', 'Door-to-Door Service'),
    ]

    SPECIALIZATIONS = {
        'medical': ["Blood Checkup", "Full Body Checkup"],
        'mechanical': ["Bike Repair", "Car Repair", "Parts Replacement"],
        'electrical': ["Wiring", "Repairing"],
        'cleaning': ["Residential Cleaning", "Deep Cleaning", "Spring Cleaning"],
        'door-to-door': ["Cloth Service"]
    }
    
    country_code_list = [("+91","🇮🇳 India (+91)"),
                        ("+1"," USA (+1)"),
                        ("+44","🇬🇧 UK (+44)"),
                        ("+61","🇦🇺 Australia (+61)"),
                        ("+81","🇯🇵 Japan (+81)"),
                        ("+49","🇩🇪 Germany (+49)"),
                        ("+33","🇫🇷 France (+33)"),
                        ("+39","🇮🇹 Italy (+39)"),
                        ("+86","🇨🇳 China (+86)"),
                        ("+7"," Russia (+7)"),
                        ("+55","🇧🇷 Brazil (+55)"),
                        ("+971","🇦🇪 UAE (+971)"),
                        ("+27","🇿🇦 South Africa (+27)"),
                        ("+92","🇵🇰 Pakistan (+92)"),
                        ("+62","🇮🇩 Indonesia (+62)"),]

    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='shopkeeper_profile')
    business_name = models.CharField(max_length=150, unique=True)
    service_type = models.CharField(max_length=25, choices=service_type_list,default="Madical")  # Add your choices here
    specializations = models.JSONField(default=list)  # Store specializations as a list

    country_code = models.CharField(max_length=25, choices=country_code_list,default="+91")  # Add your choices here
    phone = models.CharField(max_length=15, unique=True,blank=True)
    email = models.EmailField(unique=True,blank=True)


    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='shopkeeper_profile')
    business_name = models.CharField(max_length=150, unique=True)
    service_type = models.CharField(max_length=100)
    specializations = models.JSONField()
    experience = models.PositiveIntegerField()
    certification = models.CharField(max_length=100, blank=True, null=True)
    certification_file = models.FileField(upload_to='certifications/', blank=True, null=True)

    # Business Hours
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    # Location
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    profile = models.ImageField(upload_to='profiles/', blank=True, null=True)  # Ensure this exists



    # Identity Verification
    aadhar_number = models.CharField(max_length=12, unique=True)
    aadhar_file = models.FileField(upload_to='aadhar_docs/', blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    gst_number = models.CharField(max_length=15, unique=True, null=True, blank=True)  # GST Field Added


    # Payment Details
    PAYMENT_CHOICES = [
        ('bank', 'Bank Transfer'),
        ('upi', 'UPI Payment')
    ]
    payment_type = models.CharField(max_length=10, choices=PAYMENT_CHOICES)

    # Bank Details (if payment_type is bank)
    individual_name = models.CharField(max_length=100, blank=True, null=True)
    account_number = models.CharField(max_length=20, blank=True, null=True)
    ifsc_code = models.CharField(max_length=20, blank=True, null=True)

    # UPI Details (if payment_type is upi)
    upi_id = models.CharField(max_length=50, blank=True, null=True)

    is_verified = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        """Automatically filter valid specializations based on service type."""
        if self.service_type in self.SPECIALIZATIONS:
            valid_specializations = self.SPECIALIZATIONS[self.service_type]
            self.specializations = [spec for spec in self.specializations if spec in valid_specializations]
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.business_name} ({self.service_type})"




