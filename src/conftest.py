import pytest
from model_bakery import baker
from rest_framework.test import APIClient

from currency_rate.quotes.choices import CurrencyType
from currency_rate.quotes.models import Currency, CurrencyQuote


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def currency_usd(db):
    return baker.make(Currency, code=CurrencyType.DOLAR)


@pytest.fixture
def currency_quote_usd(currency_usd):
    return baker.make(CurrencyQuote, currency=currency_usd, exchange_rate=1.0)


@pytest.fixture
def vatcomply(responses, currency_usd, currency_quote_usd):
    current_date = currency_quote_usd.date.strftime('%Y-%m-%d')
    url = f'https://api.vatcomply.com/rates?base={currency_usd.code}&date={current_date}'
    resp = {
        'date': current_date,
        'base': currency_usd.code,
        'rates': {
            'EUR': 0.8829242450997704,
            'USD': 1.0,
            'JPY': 115.11566307610806,
            'BRL': 5.571340279004062,
        },
    }

    responses.add(
        responses.GET,
        url,
        status=200,
        json=resp,
    )
