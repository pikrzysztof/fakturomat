from django.contrib import admin
from .models import PrzedmiotUmowy, Firma, Faktura, JednostkaMiary, FormaPlatnosci

class PrzedmiotUmowyAdmin(admin.ModelAdmin):
	pass

admin.site.register(PrzedmiotUmowy, PrzedmiotUmowyAdmin)

class FirmaAdmin(admin.ModelAdmin):
	pass

admin.site.register(Firma, FirmaAdmin)

class FakturaAdmin(admin.ModelAdmin):
	pass

admin.site.register(Faktura, FakturaAdmin)

class JednostkaMiaryAdmin(admin.ModelAdmin):
	pass

admin.site.register(JednostkaMiary, JednostkaMiaryAdmin)

class FormaPlatnosciAdmin(admin.ModelAdmin):
	pass

admin.site.register(FormaPlatnosci, FormaPlatnosciAdmin)