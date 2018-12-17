from django.urls import path
from . import views

urlpatterns = [
	path('faktury/<int:id_faktury>/faktura.pdf', views.gen_faktura, name='view_faktura'),
	path('faktury/<int:id_faktury>', views.manage_faktura, name='manage_faktura'),
	path('', views.glowna),
	path('healthz', views.healthz, name='healthz')
]
