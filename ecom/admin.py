from django.contrib import admin
# Register your models here.
from . import models
from .models import *

admin.site.register(Countrys)
admin.site.register(Citys)
admin.site.register(Streets)

admin.site.register(Provider)
admin.site.register(Supply)

admin.site.register(Categorys)
admin.site.register(Products)

admin.site.register(Users)
admin.site.register(Orders)

admin.site.register(Couriers)
admin.site.register(Deliverys)




