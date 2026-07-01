from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone

class ShoppingCart(models.Model):
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def add_item(myuser, game):
        shopping_cart = ShoppingCart.objects.filter(myuser=myuser).first()
        if shopping_cart is None:
            shopping_cart = ShoppingCart.objects.create(myuser=myuser)
        ShoppingCartItem.objects.create(
            product_id=game.id,
            product_name=game.name,
            price=game.price,
            quantity=1,
            shopping_cart=shopping_cart
        )

    def get_number_of_items(self):
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        return len(shopping_cart_items)

    def get_total(self):
        total = Decimal(0.0)
        shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=self)
        for item in shopping_cart_items:
            total += item.price * item.quantity
        return total



class ShoppingCartItem(models.Model):
    product_id = models.IntegerField()
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    quantity = models.IntegerField(default=1)
    shopping_cart = models.ForeignKey(
        ShoppingCart,
        on_delete=models.CASCADE
    )


class Payment(models.Model):
    credit_card_number = models.CharField(max_length=19)  # Format: 1234 5678 1234 5678
    expiry_date = models.CharField(max_length=7)  # Format: 10/2022
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(default=timezone.now)
    myuser = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               )