from django.shortcuts import render
from .models import *
from django.http import JsonResponse


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
