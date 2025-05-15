from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from .base import BaseModel
from .rolesModel import Rol


class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico, password=None, **extra_fields):
        if not correo_electronico:
            raise ValueError('El correo electrónico es obligatorio')
        
        correo_electronico = self.normalize_email(correo_electronico)
        user = self.model(correo_electronico=correo_electronico, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, correo_electronico, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        
        return self.create_user(correo_electronico, password, **extra_fields)


class Usuario(AbstractBaseUser, PermissionsMixin, BaseModel):
    TIPO_DOCUMENTO_CHOICES = (
        ('CC', 'Cédula de Ciudadanía'),
        ('CE', 'Cédula de Extranjería'),
        ('TI', 'Tarjeta de Identidad'),
        ('PP', 'Pasaporte'),
    )
    
    nombre = models.CharField(max_length=100)
    tipo_documento = models.CharField(max_length=2, choices=TIPO_DOCUMENTO_CHOICES)
    documento = models.CharField(max_length=20, unique=True)
    direccion = models.CharField(max_length=200)
    celular_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="El número de celular debe estar en formato: '+999999999'. Hasta 15 dígitos permitidos."
    )
    celular = models.CharField(validators=[celular_regex], max_length=15)
    correo_electronico = models.EmailField(unique=True)
    rol = models.ForeignKey(Rol, on_delete=models.PROTECT)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    
    objects = UsuarioManager()
    
    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre', 'tipo_documento', 'documento', 'celular']
    
    def __str__(self):
        return f"{self.nombre} ({self.correo_electronico})"