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
            req.keywords = keyword
            if 'request' not in request.POST:
                req.donation = True
            req.phone_num = form_data.get('phone', '')
            req.description = form_data.get('description', '')
            # print("Request: " + req.person_name + " " + req.keywords + \
            #       " " + req.description + " " + req.phone_num)
        req.save()
        context['success'] = True
    return render(request, 'dashboard/index.html', context)
