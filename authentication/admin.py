from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Profile,Feedback,ContactServices,ShopkeeperProfile
from django.utils.timesince import timesince
from django.utils.timezone import now
from django.utils.html import format_html


class ProfileAdmin(UserAdmin):
    # Display these fields in the admin panel
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('gender', 'city', 'bio',"profile_image",'user_type')}),
    )

    list_display = ["username","email","Full_Name","gender","city","Active","User_Type","Profile"]
    list_display = ("username", "email", "first_name", "last_name")
    search_fields = ("username", "email", "first_name", "last_name")

    def Full_Name(self,obj):
        return f"{obj.first_name} {obj.last_name}"

    def Profile(self,obj):
        image = f"<img src='/media/{obj.profile_image}' style='width:70px;height:70px;border-radius:50%;' />"
        return format_html(image)
    
    def Active(self,instance):
        return f"{instance.is_active}"

    def User_Type(self,instance):
        if instance.is_superuser:
            return "Super"
        elif instance.is_staff:
            return "Staff"
        else:
            return "Normal"
            

# Register the custom user model

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'content', 'rating', 'real', 'created_date')
    search_fields = ('user__username', 'content')
    list_filter = ('rating', 'real', 'created_date')



class ContactAdmin(admin.ModelAdmin):
    list_display = ('Name', 'email', 'subject', 'message', 'created_date')

    def Name(self,instance):
        return str(instance.name).title()


@admin.register(ShopkeeperProfile)
class ShopkeeperAdmin(admin.ModelAdmin):
    list_display = ('user','business_name','phone', 'city', 'state', 'pincode', 'opening_time', 'closing_time')  # Display essential fields in the list view
    search_fields = ('business_name', 'service_type', 'phone', 'city', 'state')  # Enable search functionality
    list_filter = ('service_type', 'city', 'state')  # Allow filtering based on service type and location
    ordering = ('business_name',)  # Order by business name

    # Organizing Fields in the Admin Form
    fieldsets = (
        ('Business Details', {
            'fields': ('user','business_name', 'service_type', 'specializations', 'experience', 'certification', 'certification_file')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'country_code', 'street', 'city', 'state', 'pincode')
        }),
        ('Business Timings', {
            'fields': ('opening_time', 'closing_time')
        }),
        ('Verification Details', {
            'fields': ('gst_number','aadhar_number', 'aadhar_file', 'profile')
        }),
        ('Payment Details', {
            'fields': ('payment_type', 'individual_name', 'account_number', 'ifsc_code', 'upi_id')
        }),
    )

    # Customizing how specializations appear
    # filter_horizontal = ('specializations',)

    # Read-only fields (if any)
    # readonly_fields = ('certification_file', 'profile')  # Prevent accidental overwrites



admin.site.register(Profile, ProfileAdmin)
admin.site.register(ContactServices,ContactAdmin)