from django.shortcuts import render, get_object_or_404, redirect
from category.models import Category
from .models import Product, ReviewRating

from django.db.models import Q

from django.core.paginator import Paginator

from django.http import HttpResponse

from carts.models import CartItem
from carts.views import _cart_id
from .forms import ReviewForm
from django.contrib import messages

from orders.models import OrderProduct

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
    
    if request.user.is_authenticated:
        try:
            # orderproduct = OrderProduct.objects.filter(user_id=request.user.id, product_id=single_object.id)
            orderproduct = OrderProduct.objects.filter(user_id=request.user.id, product_id=single_object.id).exists() 
        except:
            orderproduct = None
    else:
        orderproduct = None

    reviews = ReviewRating.objects.filter(user=request.user, product_id=single_object.id, status=True)

    context = {"single_object": single_object, "in_cart": in_cart, "orderproduct": orderproduct, "reviews": reviews}
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



def submit_review(request, product_id):
    url = request.META.get('HTTP_REFERER')
    product_obj = get_object_or_404(Product, id=product_id)
    if request.method == "POST":
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_obj.id)
            form = ReviewForm(request.POST, instance=reviews)
            if form.is_valid():
                form.save()
                messages.success(request, "Thank you! your review has been updated")
                return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data["subject"]
                data.rating = form.cleaned_data["rating"]
                data.review = form.cleaned_data["review"]
                data.ip = request.META.get("REMOTE_ADDR")
                data.product_id = product_obj.id
                data.user_id = request.user.id
                data.save()
                messages.success(request, "Thank you! your review has been submitted")
                return redirect(url)

                # data = form.save(commit=False)

                # data.ip = request.META.get("REMOTE_ADDR")
                # data.product_id = product_id
                # data.user_id = request.user.id
                # data.save()
                # messages.success(request, "Thank you! your review has been submitted")
                # return redirect(url)