from django.contrib import admin
from .models import Place , Category
# Register your models here.

admin.site.register([Place,Category])