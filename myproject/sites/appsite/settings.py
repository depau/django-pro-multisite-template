"""Django settings.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from myproject.settings.common import *
from myproject.utils.django import add_boilerplate_settings

add_boilerplate_settings(__name__)

# Application definition
INSTALLED_APPS = COMMON_APPS + [
    "myproject.apps.core",
    "myproject.apps.mybusinesslogic",
]
