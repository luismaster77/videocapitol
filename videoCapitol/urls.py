from django.conf.urls import url
from videoCapitol import views, models
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.base, name='base'),
    url(r'^pelicula/$', views.PeliculaListView.as_view(), name='pelicula-list'),
    url(r'^pelicula/(?P<pk>\d+)/detail/$', views.PeliculaDetailView.as_view(), name='pelicula-detail'),
    url(r'^pelicula/(?P<pk>\d+)/update/$', views.PeliculaUpdate.as_view(),name='pelicula-update'),
    #Create
    url(r'^pelicula/create/$', views.PeliculaCreate.as_view(), name='pelicula-create'),
    #Delete
    url(r'^pelicula/(?P<pk>\d+)/delete/$', views.PeliculaDelete.as_view(), name='pelicula-delete'),
    #Reservar
    url(r'^pelicula/reservada/$', views.reservar_pelicula, name='reservar'),
]