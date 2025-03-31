"""
URL configuration for mainserver project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static
from authentication.views import *
from home.views import *
# from login_singup.views import *


urlpatterns = [
    path("", include("allauth.urls")),
    path('<slug>/profile/',ProfileUpdate.as_view(),name='update_profile'),
    path('profile/',redirectProfile,name='profile'),
    path("<str:user>/portfolio/",sportfolio,name="portfolio"),
    path('business_register/', businessSignup, name='business_register'),
    # path('sportfolio_profile/',sportfolio_profile,name='sportfolio_profile'),

    path('business_signup/', user_business_register, name='business_signup'),
    path('business_signin/', user_business_login, name='business_signin'),
    path('business_logout/', user_business_logout, name='business_logout'),
    path('business-Dashboard/', businessDashboard, name='business_dashboard'),
]