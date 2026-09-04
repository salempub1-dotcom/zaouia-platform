from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.home, name="home"),
    path("contents/", views.content_list, name="contents"),
    path("contents/<str:slug>/", views.content_detail, name="content_detail"),
    path("contents/<str:slug>/favorite/", views.favorite_toggle, name="favorite_toggle"),
    path("search/suggest/", views.search_suggest, name="search_suggest"),
    path("pdf/", views.pdf_library, name="pdf_library"),
    path("pdf/<str:slug>/read/", views.pdf_reader, name="pdf_reader"),
    path("scholars/", views.scholars, name="scholars"),
    path("scholars/<str:slug>/", views.scholar_detail, name="scholar_detail"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("account/", views.account, name="account"),
    path("offline/", views.offline, name="offline"),
    path("manifest.webmanifest", views.manifest, name="manifest"),
    path("sw.js", views.service_worker, name="service_worker"),
]
