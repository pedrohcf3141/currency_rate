from rest_framework import viewsets
from .models import CurrencyQuote, Currency
from .serializers import CurrencyQuoteSerializer, CurrencySerializer
from .utils import get_or_create_currency_quotes_by_dates
from django.shortcuts import render
from django.views import View
from .forms import CurrencyQuoteSearchForm

class CurrencyModelViewSet(viewsets.ModelViewSet):
   queryset = Currency.objects.all()
   serializer_class = CurrencySerializer


class CurrencyQuoteModelViewSet(viewsets.ModelViewSet):
   queryset = CurrencyQuote.objects.all()
   serializer_class = CurrencyQuoteSerializer

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
        if search_form.is_valid():
            start_date = search_form.cleaned_data.get('start_date')
            end_date = search_form.cleaned_data.get('end_date')
            code = search_form.cleaned_data.get('code')
            if start_date and end_date:
                data = get_or_create_currency_quotes_by_dates(start_date, end_date, code)
        else:
            data = []
            start_date = ''
            end_date = ''
            code = ''

        currencies = Currency.objects.all().values_list('code', flat=True)
        context = {
            'currencies': currencies,
            'start_date': start_date,
            'end_date': end_date,
            'code': code,
            'currency_quotes': data,
            'search_form': search_form,
        }
        return render(request, self.template_name, context)
