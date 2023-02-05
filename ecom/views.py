import random

from django.contrib.auth import authenticate, login, logout
from django.db.models import Sum
from django.shortcuts import render,redirect,reverse
from django.template.loader import render_to_string
from django.views import View
from reportlab.pdfgen import canvas
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from . import forms,models
from .forms import *
from .models import *
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def all_products(request):
    products = Products.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, )
    return render(request, 'allproducts.html', {'products': products})

def catalog_view(request, pk):
    products = Products.objects.filter(category__id = pk)
    return render(request, 'allproducts.html', {'products': products})

def register_view(request):
    countrys = Countrys.objects.all()
    citys = Citys.objects.all()
    streets = Streets.objects.all()
    return render(request, 'user_register.html', {'countrys': countrys, "citys":citys, "streets":streets})


def create(request):
    if request.method == "POST":
        person = Users()
        person.name = request.POST.get("name")
        person.surname = request.POST.get("surname")
        person.phone = request.POST.get("phone")

        person.country = request.POST.get("country")
        person.city = request.POST.get("city")
        person.street = request.POST.get("street")

        person.index = request.POST.get("index")
        person.house = request.POST.get("house")
        person.liter = request.POST.get("liter")
        person.apartment = request.POST.get("apartment")
        person.save()
    return HttpResponseRedirect("/")


@login_required
def profile(request):
    return render(request, 'profile.html')



def register(request):
    form = ExtendedUserForm()
    profile_form = UserProfileForm()
    if request.method == 'POST':
        form = ExtendedUserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if form.is_valid() and profile_form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = form.save()

            profile = profile_form.save(commit = False)
            profile.user = user
            profile.save()

            login(request, user, backend='django.contrib.auth.backends.ModelBackend')

            return render(request, 'welcome.html')
    context = {'form': form, 'profile_form': profile_form}
    return render(request, 'register.html', context)

@login_required
def welcome(request):
    return render(request, "welcome.html")

#### верх не трогать, вниз идёт попытки логина
from django.contrib.auth import authenticate, login


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data = request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return render(request, 'welcome.html')
    else:
        form = AuthenticationForm()
    context = { 'form': form }
    return render(request, 'login.html', context)

@login_required
def logout_view(request):
    logout(request)
    return render(request, "logout.html")

def buy_view(request, pk):
    product = Products.objects.get(id = pk)
    return render(request, 'buy.html', {'product': product})

def order_create(request, pk):
    count = Couriers.objects.all().count()
    number = random.randint(1, count)
    courier = Couriers.objects.get(id=number)
    product = Products.objects.get(id=pk)
    username = request.user.users
    if request.user.users.country == 'Kazakhstan':
        delivery = 1
    else:
        delivery = 15
    total_price = product.price + delivery
    context = {'product': product,
               'courier': courier,
               'delivery': delivery,
               'total_price': total_price,
               'user': username }
    if request.method == 'POST':
        order = Orders()
        order.user = username
        order.product = product
        order.delivery_price = delivery
        order.order_price = total_price
        order.save()
        delivery_create = Deliverys()
        delivery_create.order = order
        delivery_create.courier = courier
        delivery_create.save()
        return redirect(order_view)
    return render(request, 'order.html', context)

def order_view(request):
    orders = Orders.objects.filter(user_id = request.user.users)
    return render(request, 'user_orders.html', {'orders': orders})


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

data = {
    'company': 'Mark Company',
    'address': 'Улица Семерок',
    'city': 'Астана',
    'country': 'Казахстан',
    'index': '777666',

    'phone': '+795277777',
    'email': 'mail@mark.com',
    'website': 'myshop.com',
}

class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        orders = Orders.objects.all()
        total = Orders.objects.aggregate(Sum('order_price'))
        pdf = render_to_pdf('pdf_template.html', {'data':data,'orders':orders, 'total':total})
        return HttpResponse(pdf, content_type='application/pdf')

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        orders = Orders.objects.all()
        total = Orders.objects.aggregate(Sum('order_price'))
        pdf = render_to_pdf('pdf_template.html', {'data':data,'orders':orders, 'total':total})

        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s" % (filename)
        response['Content-Disposition'] = content
        return response

def getpdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="pdf_template.pdf"'
    p = canvas.Canvas(response)
    p.showPage()
    p.save()
    return response
