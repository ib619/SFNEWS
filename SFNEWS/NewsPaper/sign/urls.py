from django.urls import path
from .views import IndexView, upgrade_me
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('', IndexView.as_view(), name='my_account'),
    path('logout/', LogoutView.as_view(template_name='sign/logout.html'), name='logout'),
    path('upgrade/', upgrade_me, name='upgrade')
]