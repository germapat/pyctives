# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.safestring import mark_safe
from pyctivex.settings import LOGIN_TYPE_LIST, ATTRIBUTE_REQUIRED, LOGIN_LDAP


class UserManager(BaseUserManager):

    def create_user(self, username, email, login_type, document, password=None, **extra_fields):
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            login_type=login_type,
            document=document,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, login_type, document, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
            login_type=login_type,
            document=document
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    """
    Campos adicionales para el modelo de usuarios
    """
    id = models.AutoField(primary_key=True)

    login_type = models.CharField('Tipo de login', choices=LOGIN_TYPE_LIST, default=LOGIN_LDAP, max_length=20,
                                  help_text=mark_safe('{} Seleccione tipo'.format(ATTRIBUTE_REQUIRED)))

    document = models.BigIntegerField('Documento',
                                      help_text=mark_safe('{} Sólo números'.format(ATTRIBUTE_REQUIRED)))

    objects = UserManager()

    REQUIRED_FIELDS = ['email', 'login_type', 'document']

    @property
    def name(self):
        return '{} {}'.format(self.first_name, self.last_name).strip()

    class Meta:
        verbose_name_plural = 'Usuarios'
        verbose_name = 'Usuario'

        ordering = ['-document']

        # Permisos por defecto desactivados
        default_permissions = ()
        # Se crear los propios permisos y de esta forma tenerlos en español

        permissions = (
            ('add_user', 'Crear usuarios'),
            ('change_user', 'Actualizar un usuario'),
            ('list_user', 'Consultar usuarios'),
            ('retrieve_user', 'Consultar un usuario'),
            ('add_groups', 'Crear un grupo'),
            ('change_groups', 'Actualizar un grupo'),
            ('list_groups', 'Consultar grupos'),
            ('retrieve_groups', 'Consultar un grupo')
        )
