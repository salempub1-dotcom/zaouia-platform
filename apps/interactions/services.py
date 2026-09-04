from django.db import transaction
from django.db.models import F
from .models import Favorite, ViewHistory

@transaction.atomic
def toggle_favorite(user,content):
    obj,created=Favorite.objects.get_or_create(user=user,content=content)
    if not created:
        obj.delete();type(content).objects.filter(pk=content.pk,favorites_count__gt=0).update(favorites_count=F("favorites_count")-1);return False
    type(content).objects.filter(pk=content.pk).update(favorites_count=F("favorites_count")+1);return True

def touch_history(content,request):
    if request.user.is_authenticated:lookup={"user":request.user,"content":content}
    else:
        if not request.session.session_key:request.session.save()
        lookup={"user":None,"session_key":request.session.session_key,"content":content}
    return ViewHistory.objects.get_or_create(**lookup)[0]
