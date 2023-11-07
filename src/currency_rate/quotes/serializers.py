from rest_framework import serializers
from .models import CurrencyQuote, Currency


class CurrencyQuoteSerializer(serializers.ModelSerializer):
    """
    Serializer para Modelo CurrencyQuote
    """

    currency = serializers.CharField(source='currency.code')
    class Meta:
        model = CurrencyQuote
        fields = [
            'date',
            'currency',
            'exchange_rate'
        ]


class CurrencySerializer(serializers.ModelSerializer):
    """
    Serializer para Modelo Currency
    """
   
    class Meta:
       model = Currency
       fields = [
           'code',
       ]
