from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Langilea)
admin.site.register(Alergeno)
admin.site.register(Produktua)
admin.site.register(Eskaria)
admin.site.register(Iritzia)