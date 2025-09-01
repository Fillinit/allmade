import telebot
from django.conf import settings
from django.shortcuts import redirect
from .models import Main_info
from django.shortcuts import render, redirect, get_object_or_404
from .models import Main_info, Category, Product, Blog, Ip, Review, Guest_Review
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from cart.cart import Cart
from .forms import Guest_ReviewForm, ReviewForm
from django.db.models import Q


def index(request):
    template = "mainapp/index.html"
    cart = Cart(request)
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
        "product_information": Product.objects.all().order_by('-id')[:8],
        "blog_information": Blog.objects.all()[:3],
        "discount_product_information": Product.objects.all().filter(discount=True),

    }
    return render(request, template, context)


def catalog(request):
    template = "mainapp/catalog.html"
    cart = Cart(request)
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
        "category_information": Category.objects.all(),
        "product_information": Product.objects.all().order_by('-id'),
        "product_views": Product.objects.all().order_by('-views')[:12]
    }
    return render(request, template, context)


def search(request):
    template = "mainapp/catalog.html"
    cart = Cart(request)
    

    search_query = request.POST.get('name')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.none()
    
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
        "category_information": Category.objects.all(),
        "product_information": products,
        "product_views": Product.objects.all().order_by('-views')[:12],
        "search_query": search_query  # Передаем запрос в шаблон
    }
    return render(request, template, context)


def filter_product(request, category_slug):
    template = "mainapp/catalog.html"
    cart = Cart(request)
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
        "product_information": Product.objects.all().filter(category__slug=category_slug),
        "product_views": Product.objects.all().order_by('-views')[:12],
        "category_information": Category.objects.all(),
    }
    return render(request, template, context)


def single_product(request, category_slug, product_pk):
    template = "mainapp/single_product.html"
    cart = Cart(request)
    product = get_object_or_404(Product, pk=product_pk)
    product_views = Product.objects.all().order_by('-views')[:12]
    stars = list(Review.objects.filter(product__pk=product_pk, is_public=1).values('stars'))
    sum_stars = 0
    static_stars = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}

    for a in stars:
        key = a['stars']
        static_stars[key] += 1

    for a in stars:
        sum_stars += a['stars']

    try:
        sum_stars = sum_stars / len(stars)
    except ZeroDivisionError :
        sum_stars = sum_stars / 1

    if product.views == None:
        product.views = 1
        product.save()
    else:
        product.views += 1
        product.save()

    context = {
        'static_stars': static_stars,
        'sum_stars': "{:.2f}".format(sum_stars),
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
        "product_information": product,
        "product_views": product_views,
        "guest_review_views": Guest_Review.objects.filter(product__pk=product_pk),
        "review_views": Review.objects.filter(product__pk=product_pk),

    }
    return render(request, template, context)


def blog(request):
    template = "mainapp/blog.html"
    cart = Cart(request)
    blog_info = Blog.objects.all()
    paginator = Paginator(blog_info, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
        "page_obj": page_obj,
        "last_post": Blog.objects.all().order_by('-id')[:5],
    }
    return render(request, template, context)


def single_blog(request, blog_pk):
    template = "mainapp/single_blog.html"
    cart = Cart(request)
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
        "blog_info": get_object_or_404(Blog, pk=blog_pk),
        "last_post": Blog.objects.all().order_by('-id')[:5],
    }
    return render(request, template, context)


def register(request):
    cart = Cart(request)
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
    }
    if request.method == 'POST':
        user = User.objects.create_user(
            request.POST["username"],
            request.POST["email"],
            request.POST["password"])
        user.first_name = request.POST["name_fio"]
        user.last_name = request.POST["surname"]
        if request.POST["password"] == request.POST["password2"]:
            user.save()
            user = authenticate(username=request.POST["username"], password=request.POST["password"])
            login(request, user)
            return redirect('mainapp:index')
        else:
            template = "mainapp/register.html"
            return render(request, template, context)
    else:
        template = "mainapp/register.html"
        return render(request, template)


def login_in(request):
    cart = Cart(request)
    template = "mainapp/login_in.html"
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
    }
    if request.method == 'POST':
        user = authenticate(username=request.POST["username"], password=request.POST["password"])
        login(request, user)
        if user is not None:
            return redirect('mainapp:index')
        else:
            return render(request, template, context)
    else:
        return render(request, template, context)


def log_out(request):
    logout(request)
    return redirect('mainapp:index')


def contacts(request):
    template = "mainapp/contacts.html"
    cart = Cart(request)
    context = {
        "cart_len": cart.__len__(),
        "main_information": Main_info.objects.all(),
    }
    return render(request, template, context)


def contact_msg(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        try:
            main_info = Main_info.objects.first()
            if main_info:
                chat_id = main_info.id_group
                msg_text = f"""
                    📨 *Новое сообщение с сайта* 📨
                    
👤 *Имя:* {name}
📧 *Email:* `{email}`

📝 *Сообщение:*
_{message}_
"""
        
                bot = telebot.TeleBot(settings.TG_TOKEN)
                bot.send_message(chat_id, msg_text)
                
        except Exception as e:
            print(f"Ошибка при отправке сообщения в Telegram: {e}")
    
    return redirect('mainapp:contacts')


def call_msg(request):
    phone = request.POST.get('phone')
    try:
        main_info = Main_info.objects.first()
        if main_info and main_info.id_group:
            chat_id = main_info.id_group
            msg_text = f"""
📞 *Новая заявка на звонок!* 📞

🔢 *Номер телефона:* `{phone}`
"""
            bot = telebot.TeleBot(settings.TG_TOKEN)
            bot.send_message(chat_id, msg_text, parse_mode='Markdown')
            
    except Exception as e:
        bot.send_message(chat_id, f"Ошибка при отправке заявки: {e}", parse_mode='Markdown')
        
    return redirect('mainapp:index')
       



def confirmation(request):
    template = "mainapp/confirmation.html"
    return render(request, template)


def comment_guest(request, catalog_pk, product_pk):
    if request.method == 'POST':
        form = Guest_ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_pk
            review.save()
        
    return redirect('mainapp:single_product', category_slug=review.product.category.slug, product_pk=product_pk)


def comment(request, catalog_pk, product_pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product_id = product_pk
            review.save()
    
    return redirect('mainapp:single_product', category_slug=review.product.category.slug, product_pk=product_pk)
