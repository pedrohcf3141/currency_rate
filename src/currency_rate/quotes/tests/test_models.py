def test_currency_model(currency_usd):
    assert str(currency_usd) == currency_usd.code


def test_currency_quote_model(currency_quote_usd):
    assert str(currency_quote_usd) == f'{currency_quote_usd.date} - {currency_quote_usd.currency}'
