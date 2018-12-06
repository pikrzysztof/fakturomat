from django.urls import path
from . import views

urlpatterns = [
	path('faktury/<int:id_faktury>', views.manage_faktura),
	path('faktury/<int:id_faktury>/faktura', views.gen_faktura),
	path('healthz', views.healthz, name='healthz')
]
