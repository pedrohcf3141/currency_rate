from django import forms
from workadays import workdays
from .models import Currency
from .choices import CurrencyType

class CurrencyQuoteSearchForm(forms.Form):
    start_date = forms.DateField(label='Data de Início', required=False)
    end_date = forms.DateField(label='Data de Término', required=False)
    code = forms.ChoiceField(
        label='Código da Moeda',
        widget=forms.Select,
        required=True,
        initial=CurrencyType.DOLAR
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        currency_choices = Currency.objects.values_list('code', 'code')
        self.fields['code'].choices = currency_choices

    def is_valid(self):
        valid = super().is_valid()
        if not valid:
            # Se o formulário não for válido, defina cleaned_data com valores padrão vazios
            self.cleaned_data = {
                'start_date': None,
                'end_date': None,
                'code': None
            }
        return valid

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        codes = cleaned_data.get('code')
        
        if start_date and end_date and start_date > end_date:
            self.add_error('end_date', 'A Data de Término deve ser posterior à Data de Início.')

        if start_date and end_date:
            working_days = workdays.networkdays(start_date, end_date, country='BR') + 1
            if working_days > 5:
                self.add_error('end_date', 'A Data de Término deve estar dentro de 5 dias úteis.')

        return cleaned_data

