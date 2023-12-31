from django.urls import include, path
from rest_framework.schemas import get_schema_view

from .swagger import SwaggerView
from currency_rate.quotes.views import CurrencyQuoteListView

urlpatterns = [
    path(
        'api/',
        include(
            [
                path('quotes/', include('currency_rate.quotes.urls')),
            ]
        ),
    ),
    path(
        'openapi/',
        get_schema_view(title='Documentação - DESAFIO DEV. BR MED API'),
        name='openapi-schema',
    ),
    path('swagger/', SwaggerView.as_view(), name='swagger-ui'),
    path('', CurrencyQuoteListView.as_view(), name='index'),
]
