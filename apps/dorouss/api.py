from django.urls import include, path
from rest_framework import routers, serializers, viewsets
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .models import Content

class ContentSerializer(serializers.ModelSerializer):
    thumbnail_url=serializers.CharField(read_only=True)
    class Meta:model=Content;fields=("id","slug","title","content_type","short_description","thumbnail_url","release_year","published_at","views_count","downloads_count","youtube_id")
class ContentViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field="slug";serializer_class=ContentSerializer;queryset=Content.objects.none();filterset_fields=("content_type","scholar__slug","category__slug","occasion__slug","release_year","is_featured");ordering_fields=("published_at","views_count","downloads_count","title")
    def get_queryset(self):return Content.objects.published().with_relations()
router=routers.DefaultRouter();router.register("contents",ContentViewSet)
urlpatterns=[path("auth/token/",TokenObtainPairView.as_view()),path("auth/token/refresh/",TokenRefreshView.as_view()),path("",include(router.urls))]
