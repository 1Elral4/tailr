from pathlib import Path

from django.conf import settings


def test_django_settings_load_for_local_development() -> None:
    assert "core.apps.CoreConfig" in settings.INSTALLED_APPS
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
    # pytest-django replaces SQLite's on-disk name with an in-memory database
    # after database-marked tests run; both values retain the SQLite backend.
    database_name = str(settings.DATABASES["default"]["NAME"])
    assert Path(database_name).name == "db.sqlite3" or database_name.startswith(
        "file:memorydb_"
    )
    assert settings.SECRET_KEY
    assert isinstance(settings.DEBUG, bool)
