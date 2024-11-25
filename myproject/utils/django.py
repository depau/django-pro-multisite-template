import importlib
import os
import sys
from collections.abc import Generator
from typing import cast

from django.apps import AppConfig


def run_django_management(settings_module: str):
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
    print(f"Using settings module: {settings_module}")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


def get_package_name(module_name: str) -> str:
    return module_name.rsplit(".", 1)[0]


def discover_packages(
    package_name: str, anchor_package: str = get_package_name(__name__)
) -> Generator[str]:
    """Discover all packages within the given package."""
    package = importlib.import_module(package_name, anchor_package)
    # noinspection PyUnresolvedReferences
    for mod_name in package.__loader__.get_resource_reader().contents():  # type: ignore
        mod_name = cast(str, mod_name)
        if "." in mod_name or mod_name.startswith("_"):
            continue
        yield f"{package.__name__}.{mod_name}"


def get_project_apps() -> Generator[str]:
    """Get all apps in the project."""
    # Find all packages the apps package
    for mod_name in discover_packages("..apps"):
        # Get the apps module within the app package
        apps_mod_name = f"{mod_name}.apps"
        try:
            apps_mod = importlib.import_module(apps_mod_name)
        except ImportError:
            continue

        # Find and yield all AppConfig subclasses in the apps module
        for name in dir(apps_mod):
            if not name.endswith("Config"):
                continue
            app_config = getattr(apps_mod, name)
            if not isinstance(app_config, type):
                continue
            if not issubclass(app_config, AppConfig) or app_config is AppConfig:
                continue

            yield f"{apps_mod_name}.{name}"


def get_project_sites() -> Generator[str]:
    """Get all sites in the project."""
    for mod_name in discover_packages("..sites"):
        try:
            importlib.import_module(f"{mod_name}.settings")
        except ImportError:
            continue
        yield mod_name


def get_all_sites_installed_apps() -> Generator[str]:
    """Get all installed apps in all sites in the project."""
    for site in get_project_sites():
        try:
            site_settings = importlib.import_module(f"{site}.settings")
        except ImportError:
            continue

        yielded = set()

        for app in site_settings.INSTALLED_APPS:
            if app in yielded:
                continue
            yield app
            yielded.add(app)


def add_boilerplate_settings(settings_module_name: str):
    """
    Load boilerplate settings into the provided settings module.
    It will automatically generate values for:
    - ROOT_URLCONF
    - WSGI_APPLICATION
    - ASGI_APPLICATION
    """

    settings_module = importlib.import_module(settings_module_name)
    site_name = settings_module_name.rsplit(".", 1)[0]

    settings_module.ROOT_URLCONF = f"{site_name}.urls"  # type: ignore
    settings_module.WSGI_APPLICATION = f"{site_name}.wsgi.application"  # type: ignore
    settings_module.ASGI_APPLICATION = f"{site_name}.asgi:application"  # type: ignore

    print(settings_module.WSGI_APPLICATION)
