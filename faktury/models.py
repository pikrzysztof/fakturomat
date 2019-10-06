from decimal import Decimal
from django.db import models, connection
import datetime
import slownie

# FIXME: Fix on_delete relationships?
def zaokraglij(x):
        return Decimal(x).quantize(Decimal('0.01'))

class JednostkaMiary(models.Model):
        nazwa = models.CharField(max_length=30)
        
        def __str__(self):
                return self.nazwa

        class Meta:
                verbose_name_plural = "Jednostki miary"

class PrzedmiotUmowy(models.Model):

        nazwa = models.CharField(max_length=300, blank=False, null=False)
        jm = models.ForeignKey(JednostkaMiary,
                               on_delete=models.PROTECT,
                               help_text='Jednostka (metry, godziny)',
                               null=True)
        pkwiu = models.CharField(max_length=300, blank=True, null=True)

        def __str__(self):
                return f'{self.nazwa} ({self.jm.nazwa})'

        class Meta:
                verbose_name_plural = "Przedmioty umowy"


class Firma(models.Model):
        nazwa = models.CharField(max_length=300)
        adres_pierwsza_linijka = models.CharField(max_length=40,
                                                  null=True, blank=True)
        adres_druga_linijka = models.CharField(max_length=40,
                                               null=True, blank=True)
        adres_trzecia_linijka = models.CharField(max_length=40,
                                                 null=True, blank=True)
        adres_czwarta_linijka = models.CharField(max_length=40,
                                                 null=True, blank=True)
        nip = models.CharField(max_length=30)

        def __str__(self):
                return self.nazwa

        class Meta:
                verbose_name_plural = 'Firmy'


class FormaPlatnosci(models.Model):
        nazwa = models.CharField(max_length=30)

        def __str__(self):
                return f'{self.nazwa}'

        class Meta:
                verbose_name_plural = 'Formy płatności'

class Faktura(models.Model):
        wystawiajacy = models.ForeignKey(Firma, null=False,
                                         on_delete=models.PROTECT,
                                         related_name='wystawiajacy_fk')
        klient = models.ForeignKey(Firma,
                                   null=False, on_delete=models.PROTECT,
                                   related_name='klient_fk')
        pozycje = models.ManyToManyField(PrzedmiotUmowy)

        numer = models.CharField(max_length=40)

        data_sprzedazy = models.DateField(default=datetime.date.today)
        data_wystawienia = models.DateField(default=datetime.date.today)
        termin_platnosci = models.DateField(default=datetime.date.today)
        forma_platnosci = models.ForeignKey(FormaPlatnosci,
                                            on_delete=models.PROTECT)
        kiedy_oplacone = models.DateField(null=True)

        def suma_netto(self):
                pozycje = IlePozycji.objects.filter(faktura=self)
                return zaokraglij(sum([poz.netto_calosc() for poz in pozycje]))

        def suma_brutto(self):
                pozycje = IlePozycji.objects.filter(faktura=self)
                return zaokraglij(sum([poz.brutto_calosc() for poz in pozycje]))
        def slownie_brutto(self):
                return slownie.slownie_zl100gr(self.suma_brutto())

        def vat(self):
                return self.suma_brutto() - self.suma_netto()

        def __str__(self):
                return f'{self.wystawiajacy} dla {self.klient}'

        class Meta:
                verbose_name_plural = "Faktury"

class IlePozycji(models.Model):
        faktura = models.ForeignKey(Faktura, null=False,
                                    on_delete=models.DO_NOTHING)
        pozycja = models.ForeignKey(PrzedmiotUmowy, null=False,
                                    on_delete=models.DO_NOTHING)
        ile = models.DecimalField(max_digits=20, default=Decimal('1'),
                                  decimal_places=5, null=False)
        podatek_proc = models.DecimalField(max_digits=5, decimal_places=3, default=Decimal('8'),
                                           null=False)
        numer_na_fakturze = models.FloatField(null=True)
        netto = models.DecimalField(max_digits=20, default=Decimal('0'), decimal_places=5)
        wyswietlana_nazwa = models.CharField(max_length=300,
                                             null=True, blank=True)

        def netto_calosc(self):
                return zaokraglij(self.netto * self.ile)
        def brutto_calosc(self):
                return zaokraglij(self.netto_calosc() * (Decimal('1') + self.podatek_proc * Decimal('0.01')))
        def podatek_zl(self):
                return zaokraglij(self.brutto_calosc() - self.netto_calosc())
