from django.conf import settings


def test_django_settings_load_for_local_development() -> None:
    assert "core.apps.CoreConfig" in settings.INSTALLED_APPS
    assert settings.DATABASES["default"]["ENGINE"] == "django.db.backends.sqlite3"
    assert settings.DATABASES["default"]["NAME"].name == "db.sqlite3"
    assert settings.SECRET_KEY
    assert isinstance(settings.DEBUG, bool)
