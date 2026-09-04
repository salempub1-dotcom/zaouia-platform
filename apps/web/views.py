from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from apps.dorouss import selectors
from apps.dorouss.filters import ContentFilter
from apps.dorouss.models import Content, ContentType
from apps.interactions.models import DownloadHistory, Favorite, ViewHistory
from apps.interactions.services import toggle_favorite, touch_history
from apps.scholars.models import Scholar
from apps.taxonomy.models import Category, Occasion
from apps.core.models import Banner, SiteSettings
from apps.core.request import client_ip, viewer_key

from .forms import ContactForm


def _paginate(request, queryset, size=18):
    return Paginator(queryset, size).get_page(request.GET.get("page"))


def home(request):
    payload = selectors.home_payload()
    context = {
        **payload,
        "banners": Banner.objects.filter(is_active=True)[:5],
        "categories": Category.objects.filter(is_active=True, show_on_home=True, parent__isnull=True)[:8],
    }
    return render(request, "web/home.html", context)


def content_list(request):
    qs = selectors.base_published()
    query = request.GET.get("q", "").strip()
    if query:
        qs = selectors.search_contents(qs, query)
    filtered = ContentFilter(request.GET, queryset=qs)
    context = {
        "page_obj": _paginate(request, filtered.qs.distinct()),
        "filter": filtered,
        "query": query,
        "types": ContentType.choices,
        "scholars": Scholar.objects.filter(is_active=True),
        "occasions": Occasion.objects.filter(is_active=True),
        "categories": Category.objects.filter(is_active=True),
    }
    template = "web/partials/content_results.html" if request.headers.get("HX-Request") else "web/content_list.html"
    return render(request, template, context)


def content_detail(request, slug):
    content = get_object_or_404(selectors.base_published(), slug=slug)
    from apps.dorouss.services import register_view

    register_view(content, viewer_key=viewer_key(request))
    history = touch_history(content, request)
    return render(request, "web/content_detail.html", {
        "content": content,
        "history": history,
        "related": selectors.related_contents(content),
        "is_favorited": request.user.is_authenticated and Favorite.objects.filter(user=request.user, content=content).exists(),
    })


@require_POST
@login_required
def favorite_toggle(request, slug):
    content = get_object_or_404(Content.objects.published(), slug=slug)
    active = toggle_favorite(request.user, content)
    return render(request, "web/partials/favorite_button.html", {"content": content, "is_favorited": active})


def pdf_library(request):
    qs = selectors.base_published().of_type(ContentType.PDF, ContentType.BOOK).select_related("pdf_document")
    query = request.GET.get("q", "").strip()
    if query:
        qs = selectors.search_contents(qs, query)
    return render(request, "web/pdf_library.html", {"page_obj": _paginate(request, qs, 16), "query": query})


def pdf_reader(request, slug):
    content = get_object_or_404(Content.objects.published().select_related("pdf_document"), slug=slug)
    try:
        document = content.pdf_document
    except Content.pdf_document.RelatedObjectDoesNotExist as exc:
        raise Http404("لا يوجد ملف PDF") from exc
    history = touch_history(content, request)
    return render(request, "web/pdf_reader.html", {"content": content, "document": document, "history": history})


def scholars(request):
    items = Scholar.objects.filter(is_active=True).annotate(
        contents_count=Count("contents", filter=Q(contents__status="published"))
    )
    return render(request, "web/scholars.html", {"scholars": items})


def scholar_detail(request, slug):
    scholar = get_object_or_404(Scholar, slug=slug, is_active=True)
    contents = selectors.base_published().filter(scholar=scholar)
    return render(request, "web/scholar_detail.html", {"scholar": scholar, "page_obj": _paginate(request, contents)})


def about(request):
    return render(request, "web/about.html", {"settings_obj": SiteSettings.get_solo()})


def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save(commit=False).ip_address = client_ip(request)
            message = form.save()
            message.ip_address = client_ip(request)
            message.save(update_fields=["ip_address"])
            return render(request, "web/partials/contact_success.html")
    else:
        form = ContactForm()
    return render(request, "web/contact.html", {"form": form})


@login_required
def account(request):
    return render(request, "web/account.html", {
        "favorites": Content.objects.published().filter(favorited_by__user=request.user)[:8],
        "history": ViewHistory.objects.filter(user=request.user).select_related("content")[:8],
        "downloads": DownloadHistory.objects.filter(user=request.user).select_related("content")[:8],
        "notifications": request.user.notifications.select_related("content")[:8],
    })


def search_suggest(request):
    suggestions = selectors.suggest_titles(request.GET.get("q", ""), limit=6)
    return render(request, "web/partials/suggestions.html", {"suggestions": suggestions})


def offline(request):
    return render(request, "web/offline.html")


def manifest(request):
    return render(request, "web/manifest.webmanifest", content_type="application/manifest+json")


def service_worker(request):
    response = render(request, "web/sw.js", content_type="application/javascript")
    response["Service-Worker-Allowed"] = "/"
    return response
