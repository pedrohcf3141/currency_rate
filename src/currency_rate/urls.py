from django.urls import include, path
from rest_framework.schemas import get_schema_view

from .health_check import HealthCheckAPIView
from .swagger import SwaggerView


urlpatterns = [
    path(
        'api/',
        include(
            [
                path(
                    'health/',
                    HealthCheckAPIView.as_view(),
                    name='health_check',
                ),
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

]
