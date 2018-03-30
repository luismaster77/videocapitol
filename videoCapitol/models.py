# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.messages import constants
# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'Perfiles de Usuario'

class Pelicula(models.Model):
    id_pelicula = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=150, blank=True, null=True)
    actores = models.CharField(max_length=500, blank=True, null=True)
    director = models.CharField(max_length=200, blank=True, null=True)
    descripcion = models.CharField(max_length=500, blank=True, null=True)
    inventario = models.IntegerField(blank=True, null=True)
    foto = models.ImageField(upload_to='photo/')

    class Meta:
        managed = False
        db_table = 'pelicula'

    def __unicode__(self):
		return self.titulo
    
    def get_absolute_url(self):
        return reverse('pelicula-list')

    def _get_importe(self):
        return self.inventario-(self.id_pelicula)
        importe = property(_get_importe)

@receiver(post_delete, sender=Pelicula)
def peliculas_delete(sender, instance, **kwargs):
    """Borra los ficheros de las fotos que se eliminan. """
    instance.foto.delete(False)

class Reserva(models.Model):
    id_reserva = models.AutoField(primary_key=True)
    id_pelicula = models.ForeignKey(Pelicula, models.DO_NOTHING, db_column='id_pelicula', blank=True, null=True)
    id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='id_usuario', blank=True, null=True)
    reserva = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'reserva'

    def __unicode__(self): 
        return '{}'.format(self.id_reserva)

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=150, blank=True, null=True)
    nombre = models.CharField(max_length=150, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    telefono = models.CharField(max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'usuario'

    def __unicode__(self):
		return self.nombre