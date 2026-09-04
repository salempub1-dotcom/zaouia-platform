from django.core.cache import cache
from .models import SiteSettings

def site_settings(request):
    value = cache.get("site_settings") or SiteSettings.get_solo()
    cache.set("site_settings", value, 600)
    return {"site_settings": value}
