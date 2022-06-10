from django.shortcuts import render
from .forms import SubscriberForm
from products.models import *


def landing(request):
    form = SubscriberForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        data = form.cleaned_data
        new_form = form.save()
    return render(request, 'landing/landing.html', locals())


def home(request):
    productsImages = ProductImage.objects.filter(isActive=True, isMain=True)
    products_category = ProductCategory.objects.filter(isActive=True)
    products_in_categories = []
    for category in products_category:
        products_images_category = productsImages.filter(product__category__name=category)
        products_in_categories.append(products_images_category)
    return render(request, 'landing/home.html', locals())