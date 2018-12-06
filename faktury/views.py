from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Faktura
from django.template.loader import get_template
import os

import sys

# Create your views here.

def manage_faktura(request, id_faktury):
	faktura = get_object_or_404(Faktura, pk=id_faktury)
	slownik = { 'faktura': faktura}

	return render(request, 'formularz.html', slownik)

def przygotuj_fakture(id, request):
	os.path.isdir(str(id))
	

def gen_faktura(request, id_faktury):
	if request.method == 'POST':
		przygotuj_fakture(id_faktury, request)
	return HttpResponse(status=200)
def healthz(_request):
	return HttpResponse(status=200)