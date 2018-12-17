from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Faktura, Firma, PrzedmiotUmowy
from decimal import Decimal
import slownie
import os
import jinja2
import sys
import subprocess
import re
from math import modf

# Create your views here.

def manage_faktura(request, id_faktury):
	faktura = get_object_or_404(Faktura, pk=id_faktury)
	slownik = { 'faktura': faktura}

	return render(request, 'formularz.html', slownik)

def przygotuj_fakture(id_faktury, request):
	if not os.path.isdir(str(id_faktury)):
		os.mkdir(str(id_faktury))
	with open('szablon.tex', 'r') as szablon:
		szablonj2 = jinja2.Template(szablon.read())
	with open(os.path.join(str(id_faktury), 'faktura.tex'), mode='w') as tmpl:
		faktura = get_object_or_404(Faktura, pk=id_faktury)
		pozycje = []
		netto_total = Decimal(0)
		vat = Decimal(0)
		zipped = zip(request.POST.getlist('wyswietlana_nazwa'),
		             request.POST.getlist('ile'),
		             request.POST.getlist('podatek'),
		             request.POST.getlist('netto'),
		             request.POST.getlist('poz_id'))
		for (nazwa, ile, podatek_proc, netto, id) in zipped:
			ile = int(ile)
			przedmiot = get_object_or_404(PrzedmiotUmowy, pk=int(id))
			netto = Decimal(netto).quantize(Decimal('0.01'))
			wartosc_netto = (ile * netto).quantize(Decimal('0.01'))
			podatek_zl = (wartosc_netto * Decimal(podatek_proc) / Decimal(100)).quantize(Decimal('0.01'))

			poz = { 'wyswietlana_nazwa': nazwa,
			        'jm': przedmiot.jm.nazwa,
			        'ile': ile,
			        'netto_za_sztuke': netto,
			        'wartosc_netto': wartosc_netto,
			        'podatek_proc': podatek_proc,
			        'podatek_zl': podatek_zl,
			        'brutto': podatek_zl + wartosc_netto,
			        'nazwa' : przedmiot.nazwa,
			        }
			netto_total += wartosc_netto
			vat += podatek_zl
			pozycje.append(poz)
		#import pdb; pdb.set_trace()
		brutto_total = vat + netto_total
		slownik = {
			'faktura': faktura,
			'netto_total': netto_total,
			'vat': vat,
			'slownie_brutto': slownie.slownie_zl100gr(brutto_total.quantize(Decimal('0.01'))),
			'pozycje': pozycje
		}
		tmpl.write(szablonj2.render(slownik))
	subprocess.check_call(['pdflatex', '-halt-on-error', '-output-directory',  str(id_faktury),
	                       os.path.join(str(id_faktury), 'faktura.tex')])

def gen_faktura(request, id_faktury):
	if request.method == 'POST':
		przygotuj_fakture(id_faktury, request)
	with open(os.path.join(str(id_faktury), 'faktura.pdf'), mode='rb') as faktura:
		return HttpResponse(faktura.read(), content_type='application/pdf')

def healthz(_request):
	return HttpResponse(status=200)

def glowna(_request):
	return render(_request, 'glowna.html', {'faktury': Faktura.objects.all()})


def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
    }
    regex = re.compile('|'.join(re.escape(unicode(key)) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)