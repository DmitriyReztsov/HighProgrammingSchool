import os, re
import sys

import atheris
from rest_framework.exceptions import ValidationError
from django.core.wsgi import get_wsgi_application
from django.test import Client
from django.urls import URLPattern, URLResolver, reverse, NoReverseMatch

# Добавляем путь к директории проекта в sys.path
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append("/src/code")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_project.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = get_wsgi_application()

import django

django.setup()
from user.urls import urlpatterns  # noqa


def flatten_urls(namespace, patterns):
    """Recursive call to traverse Django's urlpatterns and turn it into a list of patterns."""
    res = []
    for url in patterns:
        if isinstance(url, URLPattern):
            res.append((namespace, url))
        elif isinstance(url, URLResolver):
            app_name = None
            try:
                # For URLResolver
                app_name = url.app_name
            except AttributeError:
                try:
                    app_name = url.urlconf_module.app_name
                except AttributeError:
                    pass

            res += flatten_urls(url.namespace, url.url_patterns)
    return res


test_urls = flatten_urls(None, urlpatterns)
print("Testing the following URL patterns:")
for x in test_urls:
    print(f"\t{x}")


def test_email_validator(data):
    fdp = atheris.FuzzedDataProvider(data)
    fdp1 = atheris.FuzzedDataProvider(data)

    ad = fdp.ConsumeUnicodeNoSurrogates(96)
    dom = fdp1.ConsumeUnicodeNoSurrogates(96)
    input_email = ad + "@" + dom + ".com"
    client = Client()
    print(">>> INPUT <<<", input_email)
    response = client.post(
        path="/users/register/",
        data={"email": input_email, "password": input_email},
        content_type="application/json",
    )
    print(">>> RESPONSE REG <<<", response.data)
    response = client.post(
        path=reverse("user_login"),
        data={"email": input_email, "password": input_email},
        content_type="application/json",
    )
    print(">>> RESPONSE <<<", response.data)


atheris.Setup(sys.argv, test_email_validator)
atheris.Fuzz()
