from django.urls import path

from . views import index, SignUpView

app_name = 'sendmail'

urlpatterns = [
    path('', index, name='index'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
