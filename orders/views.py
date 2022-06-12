from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from .forms import CheckoutContactForm


def basket_adding(request):
    return_dict = dict()
    session_key = request.session.session_key
    print(request.POST)
    data = request.POST
    product_id = data.get('product_id')
    number = data.get('number')
    is_delete = data.get('isDelete')

    if is_delete:
        product = ProductInBasket.objects.filter(id=product_id).update(isActive=False)
    else:
        newProduct, created = ProductInBasket.objects.get_or_create(session_key=session_key, product_id=product_id,
                                                                    isActive=True, defaults={'number': number})
        if not created:
            newProduct.number += int(number)
            newProduct.save(force_update=True)


    productsInBasket = ProductInBasket.objects.filter(session_key=session_key, isActive=True)
    productsTotalNumber = productsInBasket.count()
    return_dict['productsTotalNumber'] = productsTotalNumber

    return_dict['products'] = list()

    for item in productsInBasket:
        productDict = dict()
        productDict['id'] = item.id
        productDict['name'] = item.product.name
        productDict['pricePerItem'] = item.pricePerItem
        productDict['number'] = item.number
        return_dict['products'].append(productDict)

    return JsonResponse(return_dict)


def checkout(request):
    session_key = request.session.session_key
    products_in_basket = ProductInBasket.objects.filter(session_key=session_key, isActive=True)
    form = CheckoutContactForm(request.POST or None)
    if request.POST:
        if form.is_valid():
            data = request.POST
            name = data['name']
            phone = data['phone']
            email = data['email']
            user, created = User.objects.get_or_create(username=phone, defaults={'first_name': name})

            order = Order.objects.create(user=user, customerName=name, customerEmail=email,  customerPhone=phone, status_id=1)

            for name, value in data.items():
                if name.startswith('product_in_basket_'):
                    product_in_basket_id = name.split('product_in_basket_')[1]
                    product_in_basket = ProductInBasket.objects.get(id=product_in_basket_id)

                    product_in_basket.number = value
                    product_in_basket.order = order
                    product_in_basket.save(force_update=True)

                    ProductInOrder.objects.create(product=product_in_basket.product, number=product_in_basket.number,
                                                  pricePerItem=product_in_basket.pricePerItem,
                                                  totalPrice=product_in_basket.totalPrice, order=order)
                    ProductInBasket.objects.filter(session_key=session_key, id=product_in_basket_id).update(isActive=False)
        print(request.POST)
    return render(request, 'orders/checkout.html', locals())