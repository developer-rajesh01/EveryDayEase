from django.urls import path,include
from home.views import *

urlpatterns = [
    path("",home,name="home"),
    path("services/",servicesView,name="services"),    
    path("services/search/",searchServices,name="search"),
    path("services/<str:slug>/",servicesCategory,name="services-category"),
    path("services/<str:slug>/<int:id>/<str:provider>/",servicesProvider,name="services-provider"),
    path("services/<str:slug>/<int:id>/<str:provider>/<str:service_name>",singleServices,name="single-service"),

    path("flow/",flow,name="flow"),
    path('about-us/',Content,name='Home'),
    path('feedback/', feedback_view, name='feedback'),
    path('contact-us/', contact_view, name='feedback'),
]
