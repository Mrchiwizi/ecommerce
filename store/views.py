from django.shortcuts import render, get_object_or_404
from category.models import Category
from .models import Product

from django.db.models import Q

from django.core.paginator import Paginator

from django.http import HttpResponse

from carts.models import CartItem
from carts.views import _cart_id

# Create your views here.


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True).filter(category=categories)
        # **********Paginator**********
        paginator = Paginator(products, 3)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # **********Paginator**********
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by("id")
        # **********Paginator**********
        paginator = Paginator(products, 4)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        # **********Paginator**********
        product_count = products.count()

    context = {"products": page_obj, "product_count": product_count}
    return render(request, "store/store.html", context)


def product_detail(request, category_slug, product_slug):
    try:
        single_object = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(product=single_object, cart__cart_id=_cart_id(request)).exists()
    except Exception as e:
        raise e
    
    context = {"single_object": single_object, "in_cart": in_cart}
    return render(request, "store/product_detail.html", context)


def search(request):
    product_count = 0
    products = None
    if "keyword" in request.GET:
        keyword = request.GET.get("keyword")
        if keyword:
            products = Product.objects.order_by("-created_date").filter(Q(product_name__icontains=keyword) | Q(description__icontains=keyword))
            
            # # **********Paginator**********
            # paginator = Paginator(products, 1)
            # page_number = request.GET.get("page")
            # page_obj = paginator.get_page(page_number)
            # # **********Paginator**********
            product_count = products.count()
    context = {"products": products, "product_count": product_count}
    return render(request, "store/store.html", context)