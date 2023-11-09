from django.urls import reverse

from currency_rate.pagination import CustomPageNumberPagination


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
