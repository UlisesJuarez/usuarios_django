from django.db import models

from django.contrib.auth.models  import AbstractBaseUser, PermissionsMixin

from .managers import UserManager


class User(AbstractBaseUser,PermissionsMixin):

    GENDER_CHOICES=(
        ('M','Masculino'),
        ('F','Femenino'),
        ('O','Otros'),
    )

    username = models.CharField(max_length=10,unique=True)
    email = models.EmailField()
    nombres = models.CharField(max_length=30,blank=True)
    apellidos = models.CharField(max_length=30,blank=True)
    genero = models.CharField(max_length=1,choices=GENDER_CHOICES,blank=True)

    USERNAME_FIELD='username'

    objects= UserManager()

    def get_short_name(self):
        return self.username
    
    def get_full_name(self):
        return self.nombres+" "+self.apellidos
    
    # def __str__(self):
    #     return self.nombres+" "+self.apellidos
