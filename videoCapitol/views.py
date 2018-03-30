# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from videoCapitol.models import Pelicula
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.core.urlresolvers import reverse_lazy
from django.template.context_processors import csrf
from forms import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import auth
from models import *
from django.template import RequestContext
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.contrib import messages
from django.contrib.messages import constants
import request
from django.db.models import F

# Create your views here.
@login_required
def base(request):
    return render(request , "base.html")

def pelicula_list(request):
    pelicula_list = Pelicula.objects.all()
    context = {'object_list': pelicula_list}
    template_name='videoCapitol/pelicula_detail.html'
    return render(request,'videoCapitol/pelicula_list.html', context)

class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls):
        return login_required(super(LoginRequiredMixin, cls).as_view())

class PeliculaListView(LoginRequiredMixin, ListView):
    model = Pelicula

class PeliculaDetailView(LoginRequiredMixin, DetailView):
    model = Pelicula

class PeliculaUpdate(UpdateView):
 login_required = True
 model = Pelicula
 fields = '__all__'

class PeliculaCreate(CreateView):
 login_required = True
 model = Pelicula 
 fields = '__all__'

class PeliculaDelete(DeleteView):
 login_required = True
 model = Pelicula
 success_url = reverse_lazy('pelicula-list')

def PeliculaReservada(request,id_pelicula):
    pelicula = Pelicula.objects.get(id_pelicula=id_pelicula)
    context = {'object': pelicula}
    return render(request,'videoCapitol/pelicula_reservado.html', context)
    

@login_required
def LogOut(request):
    logout(request)
    return redirect('/accounts/login')

def register_user(request):
    args = {}
    #args.update(csrf(request))
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        args['form'] = form
        if form.is_valid(): 
            form.save()  # guardar el usuario en la base de datos si es válido
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
            activation_key = hashlib.sha1(salt+email).hexdigest()            
            key_expires = datetime.datetime.today() + datetime.timedelta(2)

            #Obtener el nombre de usuario
            user=User.objects.get(username=username)

            # Crear el perfil del usuario                                                                                                                                 
            new_profile = UserProfile(user=user, activation_key=activation_key, 
                key_expires=key_expires)
            new_profile.save()

            # Enviar un email de confirmación
            email_subject = 'Account confirmation'
            email_body = "Hola %s, Gracias por registrarte. Para activar tu cuenta da clíck en este link en menos de 48 horas: http://127.0.0.1:8000/accounts/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'luiseduardoingsis@gmail.com',
                [email], fail_silently=False)

            return HttpResponseRedirect('/accounts/registration_complete')
    else:
        args['form'] = RegistrationForm()

    return render(request,'videoCapitol/registro.html')

def register_confirm(request, activation_key):
    # Verifica que el usuario ya está logeado
    if request.user.is_authenticated():
        HttpResponseRedirect('/videoCapitol/pelicula')

    # Verifica que el token de activación sea válido y sino retorna un 404
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)

    # verifica si el token de activación ha expirado y si es así renderiza el html de registro expirado
    if user_profile.key_expires < timezone.now():
        return render_to_response('videoCapitol/confirm_expired.html')
    # Si el token no ha expirado, se activa el usuario y se muestra el html de confirmación
    user = user_profile.user
    user.is_active = True
    user.save()
    return render_to_response('videoCapitol/confirm.html')

@login_required
def reservar_pelicula(request):
    if request.user.is_authenticated():
        res=Pelicula.objects.values('id_pelicula')
        codigo = request.GET.get('id_pelicula')
        query = request.GET.get('id_pelicula','11')
        if query:
            qset = (
                Q(id_pelicula=query)
            )
            results = Pelicula.objects.filter(qset)
        else:
            results = []
            #results = Q(numero_documento=query) 
        return render_to_response("videoCapitol/reservada.html", {"results":results ,"query": query})
    else:
        return HttpResponse("No tienes permisos para esta acción")
    
    @method_decorator(permission_required('usuarios.reservar',reverse_lazy('usuarios:usuarios')))
    def dispatch(self, *args, **kwargs):
        return super(reservar_pelicula, self).dispatch(*args, **kwargs)