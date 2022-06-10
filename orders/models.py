from django.db import models
from products.models import Product
from django.db.models.signals import post_save
from phonenumber_field.modelfields import PhoneNumberField


class Status(models.Model):
    name = models.CharField(max_length=24, blank=True, default=None, unique=True)
    isActive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказа'


class Order(models.Model):
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)# total price for all products in order
    customerName = models.CharField(max_length=128, blank=True, default=None)
    customerEmail = models.EmailField(blank=True, default=None)
    customerPhone = PhoneNumberField(max_length=48, blank=True, default=None)
    customerAddress = models.CharField(max_length=128, blank=True)
    comments = models.TextField(blank=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Заказ %s %s" % (self.id, self.status.name)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def save(self, *args, **kwargs):

        super(Order, self).save(*args, **kwargs)


class ProductInOrder(models.Model):
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    pricePerItem = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)#price*number
    isActive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Заказ %s" % self.product.name

    class Meta:
        verbose_name = 'Товар в заказе'
        verbose_name_plural = 'Товары в заказе'

    def save(self, *args, **kwargs):
        pricePerItem = self.product.price
        self.pricePerItem = pricePerItem
        self.totalPrice = self.number * self.pricePerItem

        super(ProductInOrder, self).save(*args, **kwargs)


def productInOrderPostSave(sender, instance, created, **kwargs):
    order = instance.order
    allProductsInOrder = ProductInOrder.objects.filter(order=order, isActive=True)

    orderTotalPrice = 0
    for item in allProductsInOrder:
        orderTotalPrice += item.totalPrice

    instance.order.totalPrice = orderTotalPrice
    instance.order.save(force_update=True)


post_save.connect(productInOrderPostSave, sender=ProductInOrder)


class ProductInBasket(models.Model):
    session_key = models.CharField(max_length=128, blank=True, default=None)
    order = models.ForeignKey(Order, blank=True, null=True, default=None, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, blank=True, null=True, default=None, on_delete=models.CASCADE)
    number = models.IntegerField(default=1)
    pricePerItem = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    totalPrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    isActive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Заказ %s" % self.product.name

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзине'

    def save(self, *args, **kwargs):
        pricePerItem = self.product.price
        self.pricePerItem = pricePerItem
        self.totalPrice = int(self.number) * self.pricePerItem

        super(ProductInBasket, self).save(*args, **kwargs)

