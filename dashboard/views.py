from django.shortcuts import render
from .models import Request


def index(request):
    KEYWORDS = ["Food", "Water", "Medicines",
                "Clothing", "Appliances", "Others"]
    context = {'keywords': KEYWORDS}
    if request.method == "POST":
        form_data = request.POST
        req = Request()
        req.person_name = form_data.get('name', '')
        req.keywords = ','.join(form_data.getlist('items', []))
        if 'request' not in request.POST:
            req.donation = True
        req.save()
        context['success'] = True
    return render(request, 'dashboard/index.html', context)
