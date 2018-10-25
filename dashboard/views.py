from django.shortcuts import render
from .models import Request


def index(request):
    KEYWORDS = ["Food", "Water", "Medicines",
                "Clothing", "Appliances", "Others"]
    context = {'keywords': KEYWORDS}
    if request.method == "POST":
        form_data = request.POST
        for keyword in form_data.getlist('items', []):
            req = Request()
            req.person_name = form_data.get('name', '')
            req.keywords = keyword.lstrip().rstrip().lower()
            if 'request' not in request.POST:
                req.donation = True
            req.phone_num = form_data.get('phone', '')
            req.description = form_data.get('description', '')
            # print("Request: " + req.person_name + " " + req.keywords + \
            #       " " + req.description + " " + req.phone_num)
            req.save()
        context['success'] = True
    return render(request, 'dashboard/index.html', context)


def show_donations(request):
    donations = Request.objects.filter(donation=True)
    print(donations)
    food_donations = donations.filter(keywords='food')
    water_donations = donations.filter(keywords='water')
    appl_donations = donations.filter(keywords='appliances')
    med_donations = donations.filter(keywords='medicines')
    clothing_donations = donations.filter(keywords='clothing')
    other_donations = donations.filter(keywords='others')
    print(food_donations)
    context = {'food': food_donations, 'water': water_donations, 'appl': appl_donations,
                'medicine': med_donations, 'clothing': clothing_donations, 'others': other_donations}
    return render(request, 'dashboard/show_donations.html', context)