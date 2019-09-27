from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Faktura, Firma, PrzedmiotUmowy, IlePozycji
from decimal import Decimal
import slownie
import os
import jinja2
import sys
import subprocess
import re
from math import modf
#from import templatetags import obetnij_zera

def obetnij_zera(num):
        return num.to_integral() if num == num.to_integral() else num.normalize()

# Create your views here.
def faktura_dir(id):
        return os.path.join('gen_faktury', str(id))

# wyswietla strone do wypelnienia IlePozycji
@login_required
def manage_faktura(request, id_faktury):
        faktura = get_object_or_404(Faktura, pk=id_faktury)
        ilepoz = []
        for poz in faktura.pozycje.all():
                obj, created = IlePozycji.objects.get_or_create(faktura=faktura, pozycja=poz)
                ilepoz.append(obj or created)
        slownik = { 'faktura': faktura, 'ilepoz': ilepoz}
        return render(request, 'formularz.html', slownik)

# requst to POST z rzeczami wypelnionymi w manage_faktura
@login_required
def przygotuj_fakture(request, id_faktury):
        with open('szablon.tex', 'r') as szablon:
                szablonj2 = jinja2.Template(szablon.read())
        if not os.path.isdir(faktura_dir(id_faktury)):
                os.mkdir(faktura_dir(id_faktury))
        # zapisac rzeczy ktore dostalismy z POSTa
        zipped = zip(request.POST.getlist('wyswietlana_nazwa'),
                     request.POST.getlist('ile'),
                     request.POST.getlist('podatek'),
                     request.POST.getlist('netto'),
                     request.POST.getlist('poz_id'))
        faktura = get_object_or_404(Faktura, pk=id_faktury)
        for (nazwa, ile, podatek_proc, netto, id) in zipped:
                IlePozycji.objects.filter(pk=id).update(ile=obetnij_zera(Decimal(ile)),
                                                        podatek_proc=obetnij_zera(Decimal(podatek_proc)),
                                                        netto=Decimal(netto).quantize(Decimal('0.01')),
                                                        wyswietlana_nazwa=nazwa)
        poz = IlePozycji.objects.filter(faktura=faktura)
        slownik = {'faktura': faktura,
                   'pozycje': poz}
        # i dopiero teraz wypelnic ten szablon
        with open(os.path.join(faktura_dir(id_faktury), 'faktura.tex'), mode='w') as tmpl:
                tmpl.write(szablonj2.render(slownik))
        subprocess.check_call(['pdflatex', '-halt-on-error', '-output-directory',  faktura_dir(id_faktury),
                               os.path.join(faktura_dir(id_faktury), 'faktura.tex')])

# wolane kiedy sie chce zobaczyc pdfa
@login_required
def gen_faktura(request, id_faktury):
        if request.method == 'POST':
                przygotuj_fakture(request, id_faktury)
        with open(os.path.join(faktura_dir(id_faktury), 'faktura.pdf'), mode='rb') as faktura:
                return HttpResponse(faktura.read(), content_type='application/pdf')

def healthz(_request):
        return HttpResponse(status=200)

@login_required
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
