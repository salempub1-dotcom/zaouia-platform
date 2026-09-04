import pytest
from django.utils import timezone

@pytest.fixture
def content(db):
    from apps.dorouss.models import Content, ContentType
    return Content.objects.create(title="درس في التصوف",content_type=ContentType.LESSON,status="published",published_at=timezone.now(),short_description="درس تجريبي")
