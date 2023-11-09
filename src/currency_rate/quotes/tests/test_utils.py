from currency_rate.quotes.models import CurrencyQuote
from currency_rate.quotes.utils import (
    get_currency_quote_vatcomply,
    get_or_create_currency_quotes_by_dates,
)


def test_get_currency_quote_with_currency_code(vatcomply, currency_quote_usd):

    date = currency_quote_usd.date.strftime('%Y-%m-%d')
    quotes = get_currency_quote_vatcomply(date)

    assert len(quotes) == 1
    assert quotes[0]['currency_code'] == currency_quote_usd.currency.code
    assert quotes[0]['date'] == date
    assert quotes[0]['exchange_rate'] == currency_quote_usd.exchange_rate


def test_get_currency_quote_without_currency_code(vatcomply, currency_quote_usd):

    date = currency_quote_usd.date.strftime('%Y-%m-%d')
    quotes = get_currency_quote_vatcomply(date)
    assert len(quotes) == 1
    assert quotes[0]['currency_code'] == currency_quote_usd.currency.code
    assert quotes[0]['date'] == date
    assert quotes[0]['exchange_rate'] == currency_quote_usd.exchange_rate


def test_get_or_create_currency_quotes_by_dates(vatcomply, currency_quote_usd):

    start_date = currency_quote_usd.date
    end_date = currency_quote_usd.date
    currency_code = currency_quote_usd.currency.code

    response = get_or_create_currency_quotes_by_dates(start_date, end_date, currency_code)
    assert response is None
    quotes = CurrencyQuote.objects.filter(currency__code=currency_code)
    assert quotes.count() == 1
