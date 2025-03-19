from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    
    return render(request, 'shop/product_list.html', context)

def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug, category=category, available=True)
    related_products = Product.objects.filter(category=category, available=True).exclude(id=product.id)[:4]
    cart_product_form = CartAddProductForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'cart_product_form': cart_product_form
    }
    
    return render(request, 'shop/product_detail.html', context)

def search(request):
    query = request.GET.get('q')
    products = []
    
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        ).filter(available=True)
    
    context = {
        'query': query,
        'products': products
    }
    
    return render(request, 'shop/search_results.html', context)
