# ----------------------- Python basic Modules -------------------
from django.shortcuts import redirect,HttpResponse
from django.views.generic.edit import UpdateView
from authentication.models import Profile
from django.shortcuts import render
from .forms import ShopkeeperRegistrationForm,ProfileRegistrationForm
import json
from .models import ShopkeeperProfile

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib import messages


# Create your views here.
class ProfileUpdate(UpdateView):
    model = Profile
    fields = ['profile_image','username','first_name','last_name','gender','city', 'bio']
    # fields = ['profile_image']
    template_name = 'account/profile.html'

    def get_form(self, form_class=None):
        """
        Override get_form to add custom classes to the form fields.
        """
        form = super().get_form(form_class)
        # form.fields['profile_image'].widget.attrs.update({'class': 'form-control custom-profile-image'})

        # Add custom classes to each field
        form.fields['gender'].widget.attrs.update({'class': 'form-control custom-gender'})
        form.fields['profile_image'].widget.attrs.update({'class': 'form-control custom-profile-image'})
        form.fields['city'].widget.attrs.update({'class': 'form-control custom-city'})
        form.fields['bio'].widget.attrs.update({'class': 'form-control custom-bio'})
        form.fields['username'].widget.attrs.update({'class': 'form-control custom-username'})
        form.fields['first_name'].widget.attrs.update({'class': 'form-control custom-first-name'})
        form.fields['last_name'].widget.attrs.update({'class': 'form-control custom-last-name'})

        return form

    def get_object(self, queryset=None):
        return Profile.objects.get(username=self.request.user.username)

    def post(self, request, *args, **kwargs):
        self.success_url = f'/accounts/{self.request.user.username}/profile'

        print("The profile image is ",request.POST.get('profile_image'))

        return super().post(request, *args, **kwargs)

def redirectProfile(request):

    if request.user.is_authenticated :
        if request.user.user_type == "shopkeeper":
             return redirect(f"/accounts/{request.user}/portfolio")
        return redirect(f"/accounts/{request.user}/profile")
    else:
        return redirect(f"/accounts/login")


def businessSignup(request):
    if request.method == 'POST':
        form = ShopkeeperRegistrationForm(request.POST, request.FILES)
        print("The data is: ",request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.user = request.user
            object.save()
            return HttpResponse(json.dumps({"status":200}))  # Redirect to a success page after saving
        else:
            print(form.errors)
            return HttpResponse(json.dumps({"status":404}))  # Redirect to a success page after saving


    else:
        form = ShopkeeperRegistrationForm()

        return render(request,'business_signup.html',{"form":form})


# User Signup View
def user_business_register(request):
    if request.user.is_authenticated:
        if request.user.user_type == "shopkeeper":
            return redirect("business_dashboard")
    

    if request.method == "POST":
        form = ProfileRegistrationForm(request.POST)
        if form.is_valid():
            object = form.save(commit=False)
            object.user_type = "shopkeeper"
            object.save()

            messages.success(request, "Your account has been created! You can now log in.")
            return redirect("business_signin")  # Redirect to login page
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileRegistrationForm()

    return render(request, "business_register.html", {"form": form})

# User Login View
def user_business_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == "shopkeeper":
            return redirect("business_dashboard")
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)

            print("user type  is :",user.user_type)
            if user is not None:
                if user.user_type == "shopkeeper":
                    login(request, user)
                    messages.success(request, f"Welcome, {username}!")

                    new_user  = ShopkeeperProfile.objects.filter(user =  user).first()
                    print("The new user is :  " , new_user)
                    if new_user is None:
                        return redirect("business_register")  # Change "dashboard" to the page after login
                    return redirect("business_dashboard")  # Change "dashboard" to the page after login
                    
                else:
                    messages.warning(request, "No business account found ! Please check credntials ")
        else:
            messages.error(request, "Invalid username or password")

    else:
        form = AuthenticationForm()

    return render(request, "business_login.html", {"form": form})

# User Logout View
def user_business_logout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("business_signin")

def businessDashboard(request):
    return render(request,"dashboard.html")

def sportfolio(request,user):
    if request.user.is_authenticated and request.user.user_type != "shopkeeper":
        return redirect(f"/accounts/{request.user}/profile")
    elif not request.user.is_authenticated:
        return redirect(f"/accounts/login")

    return render(request,'sportfolio.html')


# def sportfolio_profile(request,user):
#     return redirect(f"sportfolio_profile.html")