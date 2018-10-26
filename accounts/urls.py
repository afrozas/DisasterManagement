from django.contrib.auth.views import LoginView
from django.urls import include, re_path, path
from .views import SignUpView, AddWatchView, marksafe

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
    re_path(
        r'^addwatch/$',
        AddWatchView.as_view(),
        name='addwatch'
    ),
    re_path(r'^marksafe/$', marksafe, name='marksafe'),
    path('', include('django.contrib.auth.urls'))
]
