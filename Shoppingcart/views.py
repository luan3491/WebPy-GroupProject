from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from ComputerGames.models import Game
from .forms import PaymentForm
from .models import ShoppingCart, ShoppingCartItem


def show_shopping_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        if 'empty' in request.POST:
            ShoppingCart.objects.get(myuser=request.user).delete()
            context = {'shopping_cart_is_empty': True,
                       'shopping_cart_items': None,
                       'amount': 0.0}
            return render(request, 'cart.html', context)
        elif 'pay' in request.POST:
            return redirect('shopping_cart_pay')

    else:
        shopping_cart_is_empty = True
        shopping_cart_items = None
        total = Decimal(0.0)
        myuser = request.user
        if myuser.is_authenticated:
            shopping_carts = ShoppingCart.objects.filter(myuser=myuser)
            if shopping_carts:
                shopping_cart = shopping_carts.first()
                shopping_cart_is_empty = False
                shopping_cart_items = ShoppingCartItem.objects.filter(shopping_cart=shopping_cart)
                total = shopping_cart.get_total()
        context = {'shopping_cart_is_empty': shopping_cart_is_empty,
                   'shopping_cart_items': shopping_cart_items,
                   'total': total}
        return render(request, 'cart.html', context)


@login_required
def change_quantity(request, item_id, action):
    item = get_object_or_404(
        ShoppingCartItem,
        id=item_id,
        shopping_cart__myuser=request.user
    )
    if action == "plus":
        item.quantity += 1
    elif action == "minus":
        item.quantity -= 1
        if item.quantity <= 0:
            item.delete()
            return redirect("cart")
    item.save()
    return redirect("cart")


@login_required(login_url='/useradmin/login/')
def pay(request):
    if not request.user.is_authenticated:
        return redirect('login')
    shopping_cart_is_empty = True
    paid = False
    form = None
    if request.method == 'POST':
        myuser = request.user
        form = PaymentForm(request.POST)
        form.instance.myuser = myuser
        if form.is_valid():
            form.save()
            paid = True
            shopping_cart = ShoppingCart.objects.get(myuser=myuser)
            for item in ShoppingCartItem.objects.filter(shopping_cart=shopping_cart):
                game = Game.objects.get(id=item.product_id)
                myuser.owned_games.add(game)
            shopping_cart.delete()
        else:
            print(form.errors)

    else:
        shopping_carts = ShoppingCart.objects.filter(myuser=request.user)
        if shopping_carts:
            shopping_cart = shopping_carts.first()
            shopping_cart_is_empty = False
            form = PaymentForm(initial={'amount': shopping_cart.get_total()})

    context = {'shopping_cart_is_empty': shopping_cart_is_empty,
               'payment_form': form,
               'paid': paid,}
    return render(request, 'paymentterminal.html', context)