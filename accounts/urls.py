from django.urls import re_path
from .views import SignUpView

urlpatterns = [
    re_path(
        r'^signup/$',
        SignUpView.as_view(),
        name='user-signup'
    ),
]
