from django.contrib.auth.views import LoginView
from django.urls import include, re_path, path
from .views import SignUpView

urlpatterns = [
    re_path(
        r'^signup/$',
        SignUpView.as_view(),
        name='signup'
    ),
    re_path(
        r'^login/$',
        LoginView.as_view(template_name='accounts/login.html'),
        name='login'
    ),
    path('', include('django.contrib.auth.urls'))
]
