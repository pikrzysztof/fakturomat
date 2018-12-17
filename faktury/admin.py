from django.contrib import admin
from .models import PrzedmiotUmowy, Firma, Faktura, JednostkaMiary, FormaPlatnosci

class PrzedmiotUmowyAdmin(admin.ModelAdmin):
	list_filter = ('jm', )
	search_fields = ('jm', 'nazwa')
	list_display = ('nazwa', 'jm')

admin.site.register(PrzedmiotUmowy, PrzedmiotUmowyAdmin)

class FirmaAdmin(admin.ModelAdmin):
	search_fields = ('nazwa', 'adres_pierwsza_linijka',
	                 'adres_druga_linijka', 'adres_trzecia_linijka',
	                 'adres_czwarta_linijka', 'nip')
	list_display = ('nazwa', 'adres_pierwsza_linijka',
	                'adres_druga_linijka', 'adres_trzecia_linijka',
	                'adres_czwarta_linijka', 'nip')
admin.site.register(Firma, FirmaAdmin)

class FakturaAdmin(admin.ModelAdmin):
	search_fields = ('wystawiajacy', 'klient',
	                 'numer', 'data_sprzedazy', 'data_wystawienia',
	                 'termin_platnosci', 'forma_platnosci')
	list_display = ('wystawiajacy', 'klient', 'numer',
	                'data_wystawienia', 'data_sprzedazy')

admin.site.register(Faktura, FakturaAdmin)

class JednostkaMiaryAdmin(admin.ModelAdmin):
	pass

admin.site.register(JednostkaMiary, JednostkaMiaryAdmin)

class FormaPlatnosciAdmin(admin.ModelAdmin):
	pass

admin.site.register(FormaPlatnosci, FormaPlatnosciAdmin)