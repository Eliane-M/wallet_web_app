from django.urls import path
from api.views.accounts.transactions import get_balance, all_transactions, withdrawal, deposit
from api.views.accounts.transaction_report import transaction_report


urlpatterns = [
    path('', all_transactions, name='transactions'),
    path('balance/', get_balance, name='get_balance'),
    path('withdraw/', withdrawal, name='create_transaction'),
    path('deposit/', deposit, name='create_transaction'),
    path('report/', transaction_report, name='transaction_report'),
]