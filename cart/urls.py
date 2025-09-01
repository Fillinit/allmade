from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('favorites/', views.favorites, name='favorites'),
    path('buy/', views.buy, name='buy'),
    path('add/<int:product_pk>/', views.cart_add, name='cart_add'),
    path('add_buy/<int:product_pk>/', views.cart_add_2, name='cart_add_2'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('clear/', views.cart_clear, name='cart_clear'),
    path('send_tg_bot/', views.send_tg_bot, name='send_tg_bot'),
]
