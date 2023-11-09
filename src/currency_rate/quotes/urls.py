from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CurrencyQuoteModelViewSet, CurrencyModelViewSet, CurrencyQuoteListView


router = DefaultRouter()
router.register(r'currencies', CurrencyModelViewSet, basename='currency')
router.register(r'currency_quotes', CurrencyQuoteModelViewSet, basename='currency-quote')


urlpatterns = [
    path('', include(router.urls)),
    path('chart/', CurrencyQuoteListView.as_view()),
]
