from django import forms
from workadays import workdays
from .models import Currency


class CurrencyQuoteSearchForm(forms.Form):
    start_date = forms.DateField(label='Data de Início')
    end_date = forms.DateField(label='Data de Término')
    code = forms.ChoiceField(
        label='Código da Moeda',
        widget=forms.Select,
        required=True,
        choices=Currency.objects.values_list('code', 'code'),
    )

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')

        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'A Data de Término deve ser posterior à Data de Início.')

        if start_date and end_date:
            working_days = workdays.networkdays(start_date, end_date, country='BR')
            if working_days >= 5:
                self.add_error('end_date', 'A Data de Término deve estar dentro de 5 dias úteis.')

        return cleaned_data
