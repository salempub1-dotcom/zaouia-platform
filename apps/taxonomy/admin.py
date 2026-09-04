from django.contrib import admin
from .models import Category, Tag, Occasion
admin.site.register([Category, Tag, Occasion])
