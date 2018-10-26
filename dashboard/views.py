import requests
from django.shortcuts import render
from .models import Request


def index(request):
    context = {'keywords': [v for _, v in Request.KEYWORDS]}
    if request.method == "POST":
        form_data = request.POST
        for keyword in form_data.getlist('items', []):
            req = Request()
            req.person_name = form_data.get('name', '')
            req.keyword = keyword.lstrip().rstrip().lower()
            req.phone_num = form_data.get('phone', '')
            req.description = form_data.get('description', '')
            ip = request.META.get('REMOTE_ADDR', None)
            if 'request' not in request.POST:
                req.donation = True
            elif ip:
                r = requests.get('http://ip-api.com/json/' + ip).json()
                req.latitude = r['lat']
                req.longitude = r['lon']
                with open('clustering/large_set.csv', 'a') as f:
                    f.write(f"{req.keyword},{r['lat']},{r['lon']}\n")
            req.save()
        context['success'] = True
    return render(request, 'dashboard/index.html', context)


def show_donations(request):
    donations = Request.objects.filter(donation=True)
    food_donations = donations.filter(keyword='food')
    water_donations = donations.filter(keyword='water')
    appl_donations = donations.filter(keyword='appliances')
    med_donations = donations.filter(keyword='medicines')
    clothing_donations = donations.filter(keyword='clothing')
    other_donations = donations.filter(keyword='others')
    context = {'food': food_donations, 'water': water_donations, 'appl': appl_donations,
               'medicine': med_donations, 'clothing': clothing_donations, 'others': other_donations}
    return render(request, 'dashboard/show_donations.html', context)
