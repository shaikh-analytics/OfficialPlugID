from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Product, ReviewRating
from .models import Contact

def home(request):
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    # Get the reviews
    reviews = None
    for product in products:
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

    context = {
        'products': products,
        'reviews': reviews,
    }
    return render(request, 'home.html', context)



def about(request):
    return render(request, 'news/about.html')

def choose_us(request):
    return render(request, 'news/choose_us.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone', '')
        subject = request.POST.get('subject', '')
        message = request.POST.get('message')
        social_media_link = request.POST.get('social_media_link', '')

        # Get user IP address
        ip_address = request.META.get('REMOTE_ADDR')

        # Create contact submission
        contact = Contact.objects.create(
            name=name,
            email=email,
            phone=phone,
            subject=subject,
            message=message,
            social_media_link=social_media_link,
            ip_address=ip_address,
            status='new'
        )

        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('contact')

    return render(request, 'news/contact.html')

def terms_and_conditions(request):
    return render(request, 'news/terms_and_conditions.html')

def faqs(request):
    return render(request, 'news/faqs.html')

def services(request):
    return render(request, 'news/services.html')
