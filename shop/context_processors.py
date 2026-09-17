from .models import Category


def nav_categories(request):
    """Makes the category list available to every template (nav + footer)
    without every view needing to pass it explicitly."""
    return {"nav_categories": Category.objects.all()}
