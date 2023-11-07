from django.db import models


class CurrencyQuote(models.Model):
    date = models.DateField()
    currency = models.ForeignKey('Currency', on_delete=models.CASCADE)
    exchange_rate = models.DecimalField(max_digits=8, decimal_places=4)

    def __str__(self):
        return f'{self.date} - {self.currency}'


class Currency(models.Model):
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.code
