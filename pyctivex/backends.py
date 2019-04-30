import logging
import requests
from django.contrib.auth.backends import ModelBackend
from .api import ActiveDirectoryApi
from .settings import LOGIN_LDAP
from .models import User


class ActiveBackend(ModelBackend):
    """
    Autenticación personalizada, se deben definir dos metodos por lo menos
    authenticate()
    get_user()

    Documentación oficial
    https://docs.djangoproject.com/en/1.11/topics/auth/customizing/#specifying-authentication-backends

    Leer los siguientes títulos para entender el proceso
        - Specifying authentication backends
        - Writing an authentication backend
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Autenticar el usuario por aplicación o directorio activo.
        Se ejecuta cuando se llama el authenticate() del paquete django.contrib.auth.autehnticate
        y debe de estar configurado en el settings (lista llamada AUTHENTICATION_BACKENDS)

        request: objecto de la petición actual
        username: username que se envió por la petición
        password: password que se envió por la petición

        :returns User | boolean
        """
        if username is None:
            username = kwargs.get(User.USERNAME_FIELD)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            User().set_password(password)
        else:
            if user.login_type == LOGIN_LDAP:
                content, status_code = ActiveDirectoryApi.login(username, password)

                if status_code == requests.codes.ok:
                    user.set_password(password)
                    user.document = content['epersonal']['document']
                    user.first_name = content['epersonal']['first_name']
                    user.last_name = content['epersonal']['last_name']
                    user.email = content['ldap']['mail']

                    user.save()
                else:
                    logging.info('ERROR consultando usuario {}'.format(username))
                    message = content.get('general', 'Error consultando LDAP')

                    from django.core.exceptions import ValidationError

                    if request and '/api/' in request.path:
                        try:
                            from rest_framework.exceptions import ValidationError
                        except ImportError:
                            raise ValidationError(message)
                        raise ValidationError({'error': message})
                    raise ValidationError(message)

            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id):
        try:
            logging.exception('User {}'.format(user_id))
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            logging.exception('User {} does not exist'.format(user_id))
            return None
