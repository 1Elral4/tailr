from datetime import date

import pytest
from django.core.exceptions import ValidationError

from core.models import DataBankEntry


@pytest.mark.django_db
def test_entry_persists_and_has_readable_summary() -> None:
    entry = DataBankEntry.objects.create(
        entry_type=DataBankEntry.EntryType.ROLE,
        title="Senior Engineer",
        organization="Acme Corp",
        raw_text="Led the platform team.",
    )

    saved = DataBankEntry.objects.get(pk=entry.pk)
    assert saved.title == "Senior Engineer"
    assert str(saved) == "[Role] Senior Engineer at Acme Corp"


@pytest.mark.django_db
def test_invalid_date_range_raises_validation_error() -> None:
    entry = DataBankEntry(
        entry_type=DataBankEntry.EntryType.PROJECT,
        title="Migration",
        raw_text="Moved a service.",
        start_date=date(2025, 2, 1),
        end_date=date(2025, 1, 1),
    )

    with pytest.raises(ValidationError, match="End date cannot be before start date"):
        entry.full_clean()


@pytest.mark.django_db
def test_json_fields_and_category_and_tag_queries() -> None:
    entry = DataBankEntry.objects.create(
        entry_type=DataBankEntry.EntryType.ACHIEVEMENT,
        title="Improved latency",
        raw_text="Reduced API latency.",
        metrics={"latency_ms": {"before": 200, "after": 80}},
        tags=["python", "performance"],
    )
    DataBankEntry.objects.create(
        entry_type=DataBankEntry.EntryType.PROJECT,
        title="Website",
        raw_text="Created a website.",
        tags=["javascript"],
    )

    entry.refresh_from_db()
    assert entry.metrics == {"latency_ms": {"before": 200, "after": 80}}
    assert entry.tags == ["python", "performance"]
    assert list(DataBankEntry.objects.by_entry_type("achievement")) == [entry]
    assert list(DataBankEntry.objects.with_tag("python")) == [entry]
    assert not DataBankEntry.objects.with_tag("django").exists()
