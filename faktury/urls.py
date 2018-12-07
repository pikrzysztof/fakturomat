from django.urls import path
from . import views

urlpatterns = [
	path('faktury/<int:id_faktury>/faktura.pdf', views.gen_faktura),
	path('faktury/<int:id_faktury>', views.manage_faktura),
	path('healthz', views.healthz, name='healthz')
]
