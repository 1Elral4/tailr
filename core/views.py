"""Views shared by the tailr application."""

from django.shortcuts import render


def home(request):
    """Render the application landing page."""
    return render(request, "home.html")
