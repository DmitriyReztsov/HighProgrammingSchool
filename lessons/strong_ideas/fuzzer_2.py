import os, re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest import mock

import atheris
from rest_framework.exceptions import ValidationError
from django.core.wsgi import get_wsgi_application

# Добавляем путь к директории проекта в sys.path
project_directory = os.path.abspath(os.path.join(os.path.dirname(__file__)))
sys.path.append("/src/code")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "a_project.settings")
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

application = get_wsgi_application()


@mock.patch("a_project.utils.core.timezone_now", return_value=None)
def test_nearest_date(data, mock_get_timezone_now):
    from a_project.utils.core import nearest_business_hour

    fdp = atheris.FuzzedDataProvider(data)
    time_zone = ZoneInfo("UTC")
    date = fdp.PickValueInList(
        [
            datetime(2024, 5, 3, 6, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 3, 7, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 3, 12, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 3, 18, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 3, 19, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 4, 6, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 4, 7, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 4, 12, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 4, 18, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 4, 19, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 5, 7, 0, 0, 0, tzinfo=time_zone),
            datetime(2024, 5, 6, 7, 0, 0, 0, tzinfo=time_zone),
        ]
    )
    # mock_get_timezone_now = mock.patch("a_project.utils.core.timezone_now", return_value=None)
    mock_get_timezone_now.return_value = date
    bh = nearest_business_hour()
    print(">>> WTF <<<", mock_get_timezone_now.return_value, bh)


atheris.Setup(sys.argv, test_nearest_date)
atheris.Fuzz()
