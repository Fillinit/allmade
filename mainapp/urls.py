from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.index, name='index'),
    path('catalog/', views.catalog, name='catalog'),
    path('search/', views.search, name='search'),
    path('catalog/<slug:category_slug>', views.filter_product, name='filter_product'),
    path('catalog/<slug:category_slug>/<int:product_pk>/', views.single_product, name='single_product'),
    path('blog/', views.blog, name='blog'),
    path('blog/<int:blog_pk>/', views.single_blog, name='single_blog'),
    path('register/', views.register, name='register'),
    path('login_in/', views.login_in, name='login_in'),
    path('logout/', views.log_out, name='logout'),
    path('contacts/', views.contacts, name='contacts'),
    path('contact_msg/', views.contact_msg, name='contact_msg'),
    path('call_msg/', views.call_msg, name='call_msg'),
    path('confirmation/', views.confirmation, name='confirmation'),
    path('comment_guest/<int:catalog_pk>/<int:product_pk>', views.comment_guest, name='comment_guest'),
    path('comment/<int:catalog_pk>/<int:product_pk>', views.comment, name='comment'),

]
