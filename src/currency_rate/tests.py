from unittest.mock import patch

from django.db.utils import OperationalError
from django.urls import reverse

from currency_rate.pagination import CustomPageNumberPagination


def test_health_check_url(client, db):
    response = client.get(reverse('health_check'))
    assert response.status_code == 200


def test_health_check_url_operationalerror(client, db):
    with patch('django.db.connection.ensure_connection', side_effect=OperationalError):
        response = client.get(reverse('health_check'))
        assert response.status_code == 503


def test_openapi_schema_url(client):
    response = client.get(reverse('openapi-schema'))
    assert response.status_code == 200


def test_swagger_ui_url(client):
    response = client.get(reverse('swagger-ui'))
    assert response.status_code == 200


def test_custom_pagination_values():
    assert CustomPageNumberPagination.page_size == 10
    assert CustomPageNumberPagination.page_size_query_param == 'page_size'
    assert CustomPageNumberPagination.max_page_size == 100
