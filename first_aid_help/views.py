from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'first_aid_help/index.html')