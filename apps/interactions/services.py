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


def save_progress(content, request, *, position, total=0, completed=False):
    history = touch_history(content, request)
    history.last_position = max(0, int(position))
    if total:
        history.total = max(0, int(total))
        history.progress_percent = min(100, int(history.last_position * 100 / history.total))
    history.completed = bool(completed or history.progress_percent >= 95)
    history.save(update_fields=["last_position", "total", "progress_percent", "completed", "last_viewed_at"])
    return history
