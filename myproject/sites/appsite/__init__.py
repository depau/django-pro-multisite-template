from myproject.utils.django import run_django_management

# Relative imports are normally not a good practice.
# We allow them in this case so the file can be copied as-is to all Django sites.
from . import settings


def manage():
    run_django_management(settings.__name__)
