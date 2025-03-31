import os
import requests
from django.core.files.base import ContentFile
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.socialaccount.models import SocialAccount
from django.core.files.storage import default_storage
# from .models import CustomUser


@receiver(post_save, sender=SocialAccount)
def update_profile_image(sender, instance, created, **kwargs):
    user = instance.user
    print("The user is : ",user)

    print(instance.provider)

    if instance.provider == 'google' and created:
        # Get the Google profile image URL
        picture_url = instance.extra_data.get('picture')
        print("The profile url is ",picture_url)
        if picture_url:
            # Download the image from the URL
            response = requests.get(picture_url)
            print("The response is ",response.content)

            if response.status_code == 200:
                # Generate a file name for the image
                file_name = f'{user.username}_profile.jpg'
                print("The filename is ",file_name)

                # Save the image as a FileField
                user.profile_image.save(file_name, ContentFile(response.content), save=True)
                user.save()
