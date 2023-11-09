import requests
from django.conf import settings
from datetime import timedelta, date, datetime
from .models import Currency, CurrencyQuote
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from .choices import CurrencyType


def get_currency_quote_vatcomply(d_date: str) -> list:
    url = f'{settings.VATCOMPLY_URL}?base={CurrencyType.DOLAR}&date={d_date}'
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        currency_codes = Currency.objects.all().values_list('code', flat=True)
        return [
            {
                'currency_code': currency_code,
                'date': response_data['date'],
                'exchange_rate': response_data['rates'][currency_code],
            }
            for currency_code in currency_codes
        ]
    else:
        print(f'Failed to get data on {date}')
        return []


def get_or_create_currency_quotes_by_dates(
    start_date: date, end_date: date, currency_code: str
) -> None:
    delta = end_date - start_date
    date_list = [(start_date + timedelta(days=i)) for i in range(delta.days + 1)]
    data = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for d_date in date_list:
            d_date.strftime('%Y-%m-%d')
            future = executor.submit(get_currency_quote_vatcomply, d_date)
            futures.append(future)
        wait(futures)
        for future in as_completed(futures):
            currencies_quotes = future.result()
            data.append(currencies_quotes)
            CurrencyQuote.objects.bulk_create(
                [
                    CurrencyQuote(
                        currency=Currency.objects.get(code=currency['currency_code']),
                        date=datetime.strptime(currency['date'], '%Y-%m-%d').date(),
                        exchange_rate=currency['exchange_rate'],
                    )
                    for currency in currencies_quotes
                ],
                update_conflicts=True,
                update_fields=['exchange_rate'],
                unique_fields=['currency', 'date'],
            )
