# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from videoCapitol.models import Pelicula,Usuario,Reserva

# Register your models here.
admin.site.register(Pelicula)
admin.site.register(Usuario)
admin.site.register(Reserva)

