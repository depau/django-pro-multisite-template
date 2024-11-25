# Django Professional Multi-Site Starter Template

Django is great for building reliable and well-architected web applications. However, setting up a modern project that
follows the current best practices can be time-consuming.

> [!NOTE]
> This template is for a **multi-site** project. Most applications only need a single site configuration.
> You can check out the simpler
> single-site [Django Professional Starter Template](https://github.com/depau/django-pro-template) if you don't need
> multi-site support.
>
> Migrating to this multi-site setup shouldn't take more than a few hours of refactoring if you change your mind along
> the way.

Use this template to start your next Django project with a solid foundation. It includes:

- A multi-site setup that allows you to serve multiple configurations from a single codebase
  - Great for organizations that have multiple flavors of the same product, or a tightly integrated product lineup!
- Follows the [Twelve-Factor App](https://12factor.net/) methodology
  - Configuration is done through environment variables
- Runs asynchronously in production with `asyncio`, [Uvicorn](https://www.uvicorn.org/)
  and [uvloop](https://uvloop.readthedocs.io/user/index.html)
- PEP-compliant: all project configuration happens in `pyproject.toml`
- Using [uv](https://docs.astral.sh/uv/) (in place of Poetry and similar tools),
  [ruff](https://docs.astral.sh/ruff/linter/) (replaces Black, isort, flake8) and [mypy](https://mypy-lang.org/) for the
  best possible Python development experience
- [Django REST Framework](https://www.django-rest-framework.org/) out of the box
  - [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/) is also included for modern OpenAPI support
  - [Django REST Auth](https://django-rest-auth.readthedocs.io/en/latest/introduction.html) for JWT authentication
  - [Django Filter](https://django-filter.readthedocs.io/en/stable/index.html) for filtering
- [Django Debug Toolbar](https://django-debug-toolbar.readthedocs.io/en/latest/installation.html) is ready to use
- [Django Health Check](https://django-health-check.readthedocs.io/en/latest/) is set up for monitoring
- [pre-commit](https://pre-commit.com/) hooks for code quality
- Dockerfile is included for easy deployment

To be added:

- Sample GitHub Actions workflow for CI/CD
- Sample `docker-compose.yml` for local development
- DevContainer support

## Make it yours

1. Clone this repository
2. Rename the `myproject` to your project name
3. Rename the apps (`core`, `mybusinesslogic`) to your app names
4. Rename the site (`appsite`) to your site name
5. Make sure to find and replace all instances of `myproject`, `mybusinesslogic`, etc. in the codebase
6. Copy `.env.sample` to `.env` and adjust the environment variables to your needs (hint:
   try [direnv](https://direnv.net/))
7. Run `uv sync --dev --extra production` to install the dependencies
8. Run `uv run python -m myproject.sites.appsite` to run management commands
9. Install the pre-commit hooks with `pre-commit install`

## Design Decisions

### Why `uv`?

`uv` is a new, PEP-compliant build tool that aims to replace Poetry and similar tools.

We chose `uv` because:

- It's incredibly fast
- It's convenient to use
- It's compliant with the latest Python packaging standards and uses `pyproject.toml` without non-standard custom
  sections

### Django site structure

For this project we adopted a peculiar site structure that comes from years of experience in building Django projects.

- `project/`: The main code base package
  - `apps/`: All the apps of the project
    - `core/`: The core app of the project, where all common models and APIs are defined
    - Other apps that are specific to the project
  - `sites/`: The sites of the project
  - `settings/`: Shared settings for all sites
  - `utils/`: Utility functions and classes that are shared across the project

The rationale behind this structure is the following:

When you're building multiple similar applications based on the same core object model it is often useful to share as
much code as possible between them.

This is especially true for settings: the difference in site settings modules between two average related Django sites
is often minimal, mostly coming down to the list of installed apps and middleware.

This setup attempts to keep the configuration DRY and move configuration to environment variables as much as possible.
