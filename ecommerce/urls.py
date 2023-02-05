from django.contrib.auth import authenticate,login
from django.contrib import admin
from django.shortcuts import render
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

from ecom import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.all_products, name=''),
    path('catalog/<int:pk>', views.catalog_view,name='catalog/pk'),

    path('register/', views.register, name='register'), #вторая версия регистра
    path('welcome/', views.welcome, name='welcome'), #привествие страница, перенаправляет из за @login_requeired

    path('login/', views.login_view, name= 'login'),
    path('logout/', views.logout_view, name= 'logout'),

    path('buy/<int:pk>/', views.buy_view, name= 'buy'),
    path('order/<int:pk>/', views.order_create, name= 'order_create'),
    path('order_view/', views.order_view, name= 'order_view'),

    path('pdf_view/', views.ViewPDF.as_view(), name="pdf_view"),
    path('pdf_download/', views.DownloadPDF.as_view(), name="pdf_download"),
    path('pdf',views.getpdf),
]

