from django.core.cache import cache
from django.db.models import Q
from .models import Content, ContentType

def base_published():return Content.objects.published().with_relations()
def search_contents(qs,q):return qs.filter(Q(title__icontains=q)|Q(short_description__icontains=q)|Q(description__icontains=q)|Q(body__icontains=q))
def related_contents(content,limit=6):return base_published().exclude(pk=content.pk).filter(Q(content_type=content.content_type)|Q(scholar=content.scholar))[:limit]
def suggest_titles(q,limit=6):return list(base_published().filter(title__icontains=q).values("slug","title","content_type")[:limit]) if len(q)>=2 else []
def home_payload():
    data=cache.get("home_payload")
    if data:return data
    qs=base_published();data={"featured":list(qs.filter(is_featured=True)[:6]),"latest_lessons":list(qs.filter(content_type__in=[ContentType.LESSON,ContentType.LECTURE])[:6]),"latest_pdfs":list(qs.filter(content_type__in=[ContentType.PDF,ContentType.BOOK])[:6]),"latest_audio":list(qs.filter(content_type__in=[ContentType.AUDIO,ContentType.POEM])[:6])};cache.set("home_payload",data,300);return data
