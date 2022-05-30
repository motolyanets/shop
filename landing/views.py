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
    productsImagesIphons = productsImages.filter(product__category__id=1)
    productsImagesMacbooks = productsImages.filter(product__category__id=2)
    productsImagesIpads = productsImages.filter(product__category__id=3)
    productsImagesAirpods = productsImages.filter(product__category__id=4)
    productsImagesWhatch = productsImages.filter(product__category__id=5)
    return render(request, 'landing/home.html', locals())