from django.shortcuts import render
from shop.models import Category, Product
from .models import FAQ
from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm
from django.contrib import messages

def home(request):
    categories = Category.objects.all()[:6]
    featured_products = Product.objects.filter(available=True)[:8]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    
    return render(request, 'main/home.html', context)

def about(request):
    return render(request, 'main/about.html')

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # Gửi email
            send_mail(
                f'Contact Form: {subject}',
                f'From: {name} <{email}>\n\n{message}',
                settings.DEFAULT_FROM_EMAIL,
                [settings.CONTACT_EMAIL],
                fail_silently=False,
            )
            
            messages.success(request, 'Cảm ơn bạn đã liên hệ với chúng tôi! Chúng tôi sẽ phản hồi sớm nhất có thể.')
            return render(request, 'main/contact_success.html')
    else:
        form = ContactForm()
    
    return render(request, 'main/contact.html', {'form': form})

def faq(request):
    faqs = FAQ.objects.all()
    return render(request, 'main/faq.html', {'faqs': faqs})

def guide(request):
    return render(request, 'main/guide.html')
