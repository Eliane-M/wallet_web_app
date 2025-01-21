from django.urls import path
from api.views.accounts.accounts import *


urlpatterns = [
    path('', create_account, name='create_account'),
]