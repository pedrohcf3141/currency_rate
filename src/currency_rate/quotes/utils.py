import requests
from datetime import timedelta, date, datetime
from .models import Currency, CurrencyQuote
from concurrent.futures import ThreadPoolExecutor, as_completed, wait
from .choices import CurrencyType

def get_currency_quote_vatcomply(current_date: str, currency_code: str = CurrencyType.DOLAR) -> list:
    url = f"https://api.vatcomply.com/rates?base={currency_code}&date={current_date}"
    response = requests.get(url)
    if response.status_code == 200:
        response_data = response.json()
        currency_codes = Currency.objects.all().values_list('code', flat=True)
        return [
            {
                'currency_code':currency_code,
                'date':response_data['date'],
                'exchange_rate':response_data['rates'][currency_code]
            }
            for currency_code in currency_codes
        ]
    else:
        print(f"Failed to get data on {current_date}")
        return []

    
def get_or_create_currency_quotes_by_dates(start_date: date, end_date: date, currency_code: str) -> None:
    delta = end_date - start_date
    date_list = set([(start_date + timedelta(days=i)) for i in range(delta.days + 1)])
    data = []
    resp = [] 
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for current_date in date_list:
            current_date.strftime("%Y-%m-%d")
            future = executor.submit(get_currency_quote_vatcomply, current_date, currency_code)
            futures.append(future)
        wait(futures)
        for future in as_completed(futures):
            currencies_quotes = future.result()
            data.append(currencies_quotes)

            if currency_code == CurrencyType.DOLAR:
                for currency in currencies_quotes:
                    c_code = Currency.objects.get(code=currency['currency_code'])
                    CurrencyQuote.objects.get_or_create(
                        currency=c_code,
                        date=datetime.strptime(currency['date'], '%Y-%m-%d').date(),
                        exchange_rate=currency['exchange_rate']
                )
    for lista in data:
        for d in lista:
            if d['currency_code'] != currency_code:
                resp.append(d)
    return resp
