from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mainapp.models import Product, Main_info
from .cart import Cart
from .forms import CartAddProductForm
import telebot


@require_POST
def cart_add(request, product_pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd["quantity"],
                 update_quantity=cd["update"])
    return redirect('cart:favorites')


@require_POST
def cart_add_2(request, product_pk):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_pk)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                 quantity=cd["quantity"],
                 update_quantity=cd["update"])
    return redirect('cart:buy')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    template = 'cart/cart_detail.html'
    context = {
        "cart_len": cart.__len__(),
        "cart": cart
    }
    return render(request, template, context)


def favorites(request):
    cart = Cart(request)
    template = "cart/favorites.html"
    context = {"cart_len": cart.__len__(),
               "cart": cart,
               "main_information": Main_info.objects.all(), }
    return render(request, template, context)



def buy(request):
    cart = Cart(request)

    if request.method == "POST":
        for key, value in request.POST.items():
            if key.startswith("qty_"):
                try:
                    product_id = key.split("_")[1]
                    quantity = int(value)
                    if quantity >= 0:
                        cart.update(product_id, quantity)
                except (IndexError, ValueError):
                    continue
        return redirect("cart:buy")  # перезагрузим корзину

    template = "cart/buy.html"
    context = {
        "cart_len": len(cart),
        "cart": cart,
        "form": CartAddProductForm(),
        "main_information": Main_info.objects.all(),
    }
    return render(request, template, context)



def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect('cart:cart_detail')


def send_tg_bot(request):
    cart = Cart(request)
    token = "5061060216:AAG3mhXr6jbpgUOUX4rxqdDzkJBHoUytTS0"
    bot = telebot.TeleBot(token)
    for item in cart:
        text = f"Имя продукта: {item['product'].name}\n" \
               f"Кол-во: {item['quantity']}" \
               f"Цена за кол-во: {item['total_price']}"
        bot.send_photo(chat_id=138786400, photo=item['product'].img, caption=text)

    bot.send_message(138786400, f"Цена за всё: {cart.get_total_price()}")
    cart.clear()
    return redirect('cart:cart_detail')
