from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^dato/$', views.Datos_list),
    url(r'^dato/(?P<pk>[0-9]+)/$', views.Dato_detail),
    url(r'^datoresumen/$', views.Datos_resumen),
    url('respuesta', views.humedad, name='respuesta'),
    url('resumen', views.resumen, name='resumen'),
]