from rest_framework import viewsets
from .models import CurrencyQuote, Currency
from .serializers import CurrencyQuoteSerializer, CurrencySerializer
from .utils import get_or_create_currency_quotes_by_dates
from django.shortcuts import render
from django.views import View
from .forms import CurrencyQuoteSearchForm
from django.db.models import CharField
from django.db.models.functions import Cast
from django.db.models import FloatField


class CurrencyModelViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class CurrencyQuoteModelViewSet(viewsets.ModelViewSet):
    queryset = CurrencyQuote.objects.all()
    serializer_class = CurrencyQuoteSerializer
    alowed_methods = ['GET']

    def list(self, request, *args, **kwargs):
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        if start_date and end_date:
            get_or_create_currency_quotes_by_dates(start_date, end_date)

        return super().list(request, *args, **kwargs)


class CurrencyQuoteListView(View):
    template_name = 'charts.html'

    def get(self, request, *args, **kwargs):
        search_form = CurrencyQuoteSearchForm(request.GET)
        context = {'search_form': search_form}
        if search_form.is_valid():
            start_date = search_form.cleaned_data.get('start_date')
            end_date = search_form.cleaned_data.get('end_date')
            code = search_form.cleaned_data.get('code')
            get_or_create_currency_quotes_by_dates(start_date, end_date, code)
            data = list(
                CurrencyQuote.objects.filter(
                    date__range=[start_date, end_date], currency__code=code
                )
                .annotate(
                    date_str=Cast('date', output_field=CharField()),
                    exchange_rate_float=Cast('exchange_rate', output_field=FloatField()),
                )
                .order_by('date')
                .values('date_str', 'exchange_rate_float', 'currency__code')
            )
            currencies = Currency.objects.values_list('code', flat=True)
            context.update(
                {
                    'currencies': currencies,
                    'start_date': start_date,
                    'end_date': end_date,
                    'code': code,
                    'currency_quotes': data,
                }
            )
        return render(request, self.template_name, context)
