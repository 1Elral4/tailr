"""Persistent career-history records used as the application's data bank."""

from django.core.exceptions import ValidationError
from django.db import models


class DataBankEntryQuerySet(models.QuerySet):
    """Convenience queries that work consistently with SQLite JSON storage."""

    def by_entry_type(self, entry_type: str):
        return self.filter(entry_type=entry_type)

    def with_tag(self, tag: str):
        """Return entries whose tag list contains ``tag``.

        SQLite does not support Django's JSON ``contains`` lookup. Filtering the
        small local data bank after fetching JSON values keeps membership
        semantics exact and returns a chainable queryset.
        """
        matching_ids = [
            entry.pk
            for entry in self.only("pk", "tags")
            if tag in entry.tags
        ]
        return self.filter(pk__in=matching_ids)


class DataBankEntry(models.Model):
    """A raw, structured record of a user's professional experience."""

    class EntryType(models.TextChoices):
        ROLE = "role", "Role"
        PROJECT = "project", "Project"
        ACHIEVEMENT = "achievement", "Achievement"
        EDUCATION = "education", "Education"
        CERTIFICATION = "certification", "Certification"
        OTHER = "other", "Other"

    entry_type = models.CharField(max_length=20, choices=EntryType.choices, db_index=True)
    title = models.CharField(max_length=255)
    organization = models.CharField(max_length=255, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    raw_text = models.TextField()
    metrics = models.JSONField(default=dict)
    tags = models.JSONField(default=list, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = DataBankEntryQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["entry_type", "is_current"]),
            models.Index(fields=["start_date", "end_date"]),
        ]
        ordering = ["-start_date", "-created_at"]

    def clean(self) -> None:
        super().clean()
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise ValidationError({"end_date": "End date cannot be before start date."})

    def __str__(self) -> str:
        organization = f" at {self.organization}" if self.organization else ""
        return f"[{self.get_entry_type_display()}] {self.title}{organization}"
