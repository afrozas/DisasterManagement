from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    KEYWORDS = ["Food", "Water", "Medicines", "Clothing", "Appliances", "Others"]
    context = {'keywords': KEYWORDS}
    if request.method == "POST":
        if 'request' in request.POST:
            print("Items Requested")
        else:
            print("Items Donated")
        print(request.POST.get('name'))
        print(request.POST.getlist('items'))
        print(request)
        return render(request, 'dashboard/index.html', context)
    else:
        return render(request, 'dashboard/index.html', context)