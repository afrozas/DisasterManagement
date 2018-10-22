from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    phone_num = forms.RegexField(regex=r'^\d{10}$',
                                 label='Phone number (required)',
                                 error_messages={'invalid': "Phone number should be of the form: 9876543210"})

    class Meta:
        model = User
        fields = ['name', 'phone_num', 'email', 'address', 'password1', 'password2']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 4, 'style': 'resize:none;'
                                             })
        }
