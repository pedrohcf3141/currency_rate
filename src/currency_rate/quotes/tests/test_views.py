from rest_framework import status
from django.urls import reverse
from django.utils import timezone


def test_currency_list(currency_usd, api_client):
    url = reverse('currency-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


def test_currency_detail(currency_usd, api_client):
    url = reverse('currency-detail', args=[currency_usd.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_currency_quote_list(currency_quote_usd, api_client):
    url = reverse('currency-quote-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


def test_currency_quote_detail(currency_quote_usd, api_client):
    url = reverse('currency-quote-detail', args=[currency_quote_usd.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_currency_quote_list_view_empty_form(api_client, currency_usd, currency_quote_usd):
    request = api_client.get(reverse('index'))
    assert request.status_code == status.HTTP_200_OK


def test_currency_quote_list_view_invalid_form_end_date_lt_statrt_date(api_client, currency_usd):
    invalid_form_data = {
        'start_date': timezone.now().date(),
        'end_date': (timezone.now() - timezone.timedelta(days=5)).date(),
        'code': 'USD',
    }

    request = api_client.get(reverse('index'), data=invalid_form_data)
    assert request.status_code == status.HTTP_200_OK
    assert not request.context[0].get('search_form').is_valid()


def test_currency_quote_list_view_invalid_form_more_5_days(api_client, currency_usd):
    invalid_form_data = {
        'start_date': timezone.now().date(),
        'end_date': (timezone.now() + timezone.timedelta(days=15)).date(),
        'code': 'USD',
    }

    request = api_client.get(reverse('index'), data=invalid_form_data)
    assert request.status_code == status.HTTP_200_OK
    assert not request.context[0].get('search_form').is_valid()
