from django.contrib import admin
from .models import Category, Email, TemplateEmail, History
# Register your models here.

admin.site.register(Category)
admin.site.register(Email)
admin.site.register(TemplateEmail)
admin.site.register(History)