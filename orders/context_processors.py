from .models import *
from products.models import ProductCategory

def getting_basket_info(request):
    session_key = request.session.session_key
    if not session_key:
        request.session['session_key'] = 123
        request.session.cycle_key()

    productsInBasket = ProductInBasket.objects.filter(session_key=session_key, isActive=True)
    productsTotalNumber = productsInBasket.count()

    return locals()


def getting_category_list(request):
    products_category_list = ProductCategory.objects.filter(isActive=True)
    return locals()