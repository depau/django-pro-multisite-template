"""Django settings to be used by linters."""

from myproject.settings.common import *
from myproject.utils.django import get_all_sites_installed_apps, get_project_apps

_PROJECT_APPS = list(get_project_apps())
_EXTERNAL_APPS = [
    i
    for i in get_all_sites_installed_apps()
    if i not in _PROJECT_APPS + COMMON_APPS and not i.startswith("myproject.apps.")
]

INSTALLED_APPS = [
    *COMMON_APPS,
    *_EXTERNAL_APPS,
    *_PROJECT_APPS,
]

for app in INSTALLED_APPS:
    while INSTALLED_APPS.count(app) > 1:
        INSTALLED_APPS.remove(app)

INSTALLED_APPS.remove("myproject.apps.openapi")
