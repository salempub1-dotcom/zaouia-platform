from django.core.cache import cache
from django.db.models import F

def register_view(content,viewer_key):
    if not cache.add(f"viewed:{content.pk}:{viewer_key}",1,1800):return False
    type(content).objects.filter(pk=content.pk).update(views_count=F("views_count")+1)
    return True
