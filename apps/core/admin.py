from django.contrib import admin
from solo.admin import SingletonModelAdmin
from .models import Banner, ContactMessage, SiteSettings

admin.site.register(SiteSettings, SingletonModelAdmin)
admin.site.register(Banner)
admin.site.register(ContactMessage)
