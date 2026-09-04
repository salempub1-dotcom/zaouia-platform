import django_filters as filters
from .models import Content, ContentType

class ContentFilter(filters.FilterSet):
    type=filters.MultipleChoiceFilter(field_name="content_type",choices=ContentType.choices)
    scholar=filters.CharFilter(field_name="scholar__slug")
    category=filters.CharFilter(field_name="category__slug")
    occasion=filters.CharFilter(field_name="occasion__slug")
    year=filters.NumberFilter(field_name="release_year")
    featured=filters.BooleanFilter(field_name="is_featured")
    class Meta:model=Content;fields=[]
