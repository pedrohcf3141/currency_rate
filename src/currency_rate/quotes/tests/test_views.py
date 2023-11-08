from rest_framework import status
from django.urls import reverse
import pytest

@pytest.mark.django_db(transaction=True)
def test_currency_list(currency_usd, api_client):
    url = reverse('currency-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


@pytest.mark.django_db(transaction=True)
def test_currency_detail(currency_usd, api_client):
    url = reverse('currency-detail', args=[currency_usd.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK



@pytest.mark.django_db(transaction=True)
def test_currency_quote_list(currency_quote_usd, api_client):
    url = reverse('currency-quote-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == 1


@pytest.mark.django_db(transaction=True)
def test_currency_quote_detail(currency_quote_usd, api_client):
    url = reverse('currency-quote-detail', args=[currency_quote_usd.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
