from django.urls import path
from api.views.wallet.transactions import get_balance


urlpatterns = [
    path('balance/', get_balance, name='get_balance'),
]