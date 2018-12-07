from django.db import models
import datetime

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

	def __str__(self):
		return f'{self.nazwa} ({self.jm.nazwa})'

	class Meta:
		verbose_name_plural = "Przedmioty umowy"


class Firma(models.Model):
	nazwa = models.CharField(max_length=300)
	adres_pierwsza_linijka = models.CharField(max_length=40, null=True, blank=True)
	adres_druga_linijka = models.CharField(max_length=40, null=True, blank=True)
	adres_trzecia_linijka = models.CharField(max_length=40, null=True, blank=True)
	adres_czwarta_linijka = models.CharField(max_length=40, null=True, blank=True)
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
	klient = models.ForeignKey(Firma, null=False, on_delete=models.PROTECT,
	                           related_name='klient_fk')
	pozycje = models.ManyToManyField(PrzedmiotUmowy)

	numer = models.CharField(max_length=40)

	data_sprzedazy = models.DateField(default=datetime.date.today)
	data_wystawienia = models.DateField(default=datetime.date.today)
	termin_platnosci = models.DateField(default=datetime.date.today)
	forma_platnosci = models.ForeignKey(FormaPlatnosci, on_delete=models.PROTECT)

	def __str__(self):
		return f'{self.wystawiajacy} dla {self.klient}'

	class Meta:
		verbose_name_plural = "Faktury"


# Create your models here.
