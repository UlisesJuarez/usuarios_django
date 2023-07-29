from typing import Any, Dict
from django.http import HttpResponse
from django.shortcuts import render
from django.core.mail import send_mail

from .forms import (
    UserRegisterForm, 
    LoginForm,
    UpdatePasswordForm,
    VerificationForm,)

from django.urls import reverse_lazy, reverse
from django.contrib.auth import authenticate, login, logout

from django.http import HttpResponseRedirect

from django.views.generic import (
    CreateView,
    View,
)

from django.views.generic.edit import(
    FormView,
)


from .models import User

from django.contrib.auth.mixins import LoginRequiredMixin

from .functions import code_generator


class UserRegisterView(FormView):

    template_name = "users/register.html"
    form_class=UserRegisterForm
    success_url="/"

    def form_valid(self, form):

        #generamos el codigo de verificacion

        codigo = code_generator()

        usuario = User.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password1'],
            #para pasar extra fields
            nombres=form.cleaned_data['nombres'],
            apellidos=form.cleaned_data['apellidos'],
            genero=form.cleaned_data['genero'],
            codregistro = codigo

            
        )
        # enviar al correo del usuario
        asunto="Confirmacion de email"
        mensaje=f"Codigo de verificación: {codigo}"
        email_remitente="uje170399@gmail.com"

        send_mail(asunto,mensaje,email_remitente,[form.cleaned_data['email'],])

        #redirigir a pantalla de validacion

        return HttpResponseRedirect(
            reverse(
                'users_app:user_verification',
                kwargs={'pk':usuario.id}
            )
        )


class LoginUser(FormView):

    template_name="users/login.html"
    form_class=LoginForm
    success_url=reverse_lazy('home_app:panel')

    def form_valid(self, form):
        user = authenticate(
           username = form.cleaned_data['username'],
           password = form.cleaned_data['password'],
       )
        
        login(self.request,user)

        return super(LoginUser,self).form_valid(form)



class LogoutView(View):

    def get(self,request, *arg, **kwargs):
        logout(request)
    
        return HttpResponseRedirect(
            reverse(
                'users_app:user_login'
            )
        )

class UpdatePassword(LoginRequiredMixin,FormView):

    template_name="users/update.html"
    form_class=UpdatePasswordForm
    success_url=reverse_lazy('users_app:user_login')
    login_url=reverse_lazy('users_app:user_login')

    def form_valid(self, form):

        usuario=self.request.user
        
        user = authenticate(
           username = usuario.username,
           password = form.cleaned_data['password1'],
       )
        
        if user:
            new_password=form.cleaned_data['password2']
            usuario.set_password(new_password)
            usuario.save()


        logout(self.request) 


        return super(UpdatePassword,self).form_valid(form)


class CodVerificationView(FormView):
    template_name="users/verification.html"
    form_class=VerificationForm
    success_url=reverse_lazy('users_app:user_login')

    def get_form_kwargs(self):
        kwargs = super(CodVerificationView,self).get_form_kwargs()
        kwargs.update({
            'pk':self.kwargs['pk'],
        })

        return kwargs

    def form_valid(self, form):
        
        #id_user=self.kwargs['pk']

        #se puede usar el get pero con ese no se puede hacer el update directamente 
        
        User.objects.filter(
            id=self.kwargs['pk']
        ).update(
            is_active = True
        )

        return super(CodVerificationView,self).form_valid(form)