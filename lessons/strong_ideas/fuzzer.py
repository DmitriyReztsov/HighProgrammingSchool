import os, re
import sys

import atheris
import django.core.exceptions as django_exceptions
from django.core.wsgi import get_wsgi_application

# Добавляем путь к директории проекта в sys.path
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append("/src/code")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_project.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = get_wsgi_application()


def test_email_validator(data):
    from user.views.user import OnboardingChecksMixin

    fdp = atheris.FuzzedDataProvider(data)

    input_email = fdp.ConsumeUnicodeNoSurrogates(sys.maxsize)
    is_valid_email = re.search("[\w\d]+@[\w\d]+.[a-z]{2,3}", input_email)
    print(">>> EMAIL <<<", bytearray(input_email, "utf-8"))

    try:
        OnboardingChecksMixin().validate_user_email(input_email)
    except Exception:
        print(">>> HERE <<<")
        # assert bool(is_valid_email) is False


atheris.Setup(sys.argv, test_email_validator)
atheris.Fuzz()
