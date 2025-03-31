from django.contrib import admin
from .models import ServiceProvider, Service, Booking, Review, Payment
from django.contrib import admin

website_name = "EveryDayEase"
admin.site.site_header = website_name+" Admin"  # Change the header text
admin.site.site_title = website_name+" Admin Panel"  # Change the title shown on the browser tab
admin.site.index_title = "Welcome to the Admin Dashboard"  # Change the dashboard index text


# Enable Search in ServiceProvider
@admin.register(ServiceProvider)
class ServiceProviderAdmin(admin.ModelAdmin):
    list_display = ("business_name", "category", "contact_number", "city", "state", "rating", "status")
    search_fields = ("business_name", "category", "city", "contact_number")  # Enable search
    autocomplete_fields = ["user"]  # Autocomplete dropdown

# Enable Search in Service
@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("service_name", "provider", "category", "price", "availability")
    search_fields = ("service_name", "provider__business_name", "category__name")  # Search by provider and category
    autocomplete_fields = ["provider"]  # Autocomplete dropdown

# Enable Search in Booking
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("service","provider","booking_date","booking_time","status_choices","status","total_price","payment_status","created_at")
    search_fields = ("servic", "provider", "status_choices","total_price","payment_status","status")  # Search by provider and category
    autocomplete_fields = ["user","service","provider"]  # Autocomplete dropdown

# Enable Search in Payments
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("booking","payment_method","amount","payment_status","transaction_id","payment_date",)
    search_fields = ("booking", "transaction_id", "amount","payment_status","payment_method","payment_date")  # Search by provider and category
    autocomplete_fields = ["user","booking"]  # Autocomplete dropdown

# Enable Search in Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user","provider","service","rating","review_text","created_at")
    search_fields = ("user","provider","service","rating","review_text","created_at")  # Search by provider and category
    autocomplete_fields = ["user","provider","service"]  # Autocomplete dropdown


# Enable Search in Category
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ("name", "description")
#     search_fields = ("name",)  # Enable category search
