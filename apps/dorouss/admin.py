from django.contrib import admin
from .models import Collection, Content, MediaFile, PDFDocument
class MediaInline(admin.TabularInline):model=MediaFile;extra=0
class PDFInline(admin.StackedInline):model=PDFDocument;extra=0;max_num=1
@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    list_display=("title","content_type","scholar","status","is_featured","published_at","views_count")
    list_filter=("content_type","status","is_featured","scholar","release_year");search_fields=("title","description");inlines=[MediaInline,PDFInline]
admin.site.register(Collection)
