from django.urls import path
from api.views.accounts.accounts import *
from api.views.accounts.category import create_category


urlpatterns = [
    path('', create_account, name='create_account'),
    path('new_category/', create_category, name='create_category'),
]