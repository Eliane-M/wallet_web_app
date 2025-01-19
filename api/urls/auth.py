from django.urls import path
from api.views.authentication.login import login_api
from api.views.authentication.logout import logout_api
from api.views.authentication.register import new_user

urlpatterns = [
    path('login/', login_api, name='login_api'),
    path('logout/', logout_api, name='logout_api'),
    path('register/', new_user, name='new_user'),
    
]