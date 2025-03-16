from django.shortcuts import render
from cargo_system.settings import STATIC_URL
from cargo_app.models import CorporateUser


def index(request):
    return render(request, 'home/home.html', {'firms': CorporateUser.objects.all()})

# Removed deprecated render_to_response and unused commented-out code
