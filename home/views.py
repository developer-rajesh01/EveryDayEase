from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse

from django.views.decorators.clickjacking import xframe_options_exempt
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from authentication.forms import FeedbackForm,ContactForm
from home.models import ServiceProvider,Service
from django.db.models import Q


# Create your views here.
def home(request):
    return render(request,"index.html")
# Create your views here.
def servicesCategory(request,slug):
    providers = ServiceProvider.objects.filter(category=slug.title())
    # providers = list(providers)+[3,4,33,2,1,5,2,5,23,55,76,90]    
    return render(request,"service_category.html",{"slug":slug,"providers":providers})

def servicesProvider(request,slug,id,provider):
    all_services = Service.objects.filter(category=slug.title(),provider = id)
    # all_services = list(all_services)+[3,4,33,2,1,5,2,5,23,55,76,90]    
    return render(request,"services_list.html",{"slug":slug,"provider":provider,'id':id,"services":all_services})

def searchServices(request):
    query = request.GET.get("q", "").strip()  # Get search query from the request

    if query:
        providers = ServiceProvider.objects.filter(
            Q(business_name__icontains=query) | 
            Q(category__icontains=query) | 
            Q(city__icontains=query) | 
            Q(state__icontains=query) | 
            Q(contact_number__icontains=query)
        )

        services = Service.objects.filter(
            Q(service_name__icontains=query) | 
            Q(description__icontains=query) | 
            Q(provider__business_name__icontains=query) | 
            Q(category__icontains=query) | 
            Q(price__icontains=query) | 
            Q(availability__icontains=query)
        )
    else:
        providers = ServiceProvider.objects.all()
        services = Service.objects.all()

    context = {
        "query": query,
        "providers": providers,
        "services": services,
    }
    return render(request, "searchpage.html", context)

def singleServices(request,slug,id,provider,service_name):
    all_services = Service.objects.filter(category=slug.title(),provider = id,service_name = service_name)
    # all_services = list(all_services)+[3,4,33,2,1,5,2,5,23,55,76,90]    
    return render(request,"single_service.html",{"slug":slug,"provider":provider,'id':id,"service_name":service_name,"services":all_services})



@xframe_options_exempt  # Allow embedding in an iframe
def servicesView(request):
    return render(request,"Services_Container.html")

@xframe_options_exempt  # Allow embedding in an iframe
def flow(request):
    return render(request,"flow.html")

def feedback_view(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user  # Assuming Profile is linked to User
            feedback.save()
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
                return JsonResponse({"message": "Feedback submitted successfully!"}, status=200)
            
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':  # AJAX request
                return JsonResponse({"errors": form.errors}, status=400)
    
    return render(request, 'feedback_form.html', {'form': FeedbackForm()})

def contact_view(request):


    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():
            form.save()
    

            name = request.POST.get("name")
            email = request.POST.get("email")
            subject = request.POST.get("subject")
            message = request.POST.get("message")

           
            try:
                # Send the email
                send_Email(name,email,subject,message,)
                messages.add_message(request, messages.SUCCESS, "Your message send successfully.")
                messages.add_message(request, messages.INFO, "Our team will connect you soon...")
                
                # return JsonResponse({"success": True, "message": "Email sent successfully."})
            except Exception as e:
                # return JsonResponse({"success": False, "message": str(e)})
                messages.add_message(request, messages.DEBUG, str(e))


            form = ContactForm()
        

    else:
        form = ContactForm()

    return render(request,'contact.html',{'form':form})

def send_Email(name,email,subject,message,):
    # Render the email template with dynamic data
    email_html_content = render_to_string("contact_email.html", {
        "name": name,
        "email": email,
        "subject": subject,
        "message": message,
    })

    email_message = EmailMessage(
    subject=f"New Contact Request: {subject}",
    body=email_html_content,
    from_email="hackingkali789@gmail.com",
    to=["monusainideveloper@gmail.com"],

    )

    email_message.content_subtype = "html"
    email_message.send()
    
def Content(request):
    return render(request,'about.html')

def  business_login(request):
    return render(request,'business_login.html')

