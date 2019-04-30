# -*- coding: utf-8 -*-


def jwt_response_payload_handler(*args, **kwargs):
    """
    Personalizar los datos que se devolveran después de que un usuario se autentique
    por medio del jwt

    Se ejecuta después de que jwt autentique el usuario. Se configura en el settings,
    en el diccionario JWT_AUTH con clave JWT_RESPONSE_PAYLOAD_HANDLER

    Leer el siguiente link para entender el proceso
    https://getblimp.github.io/django-rest-framework-jwt/#additional-settings

    token:      token generado cuando el usuario se autentico
    user:       instancia del usuario autenticado
    request:    objeto de la petición actual
    """
    user = kwargs.get('user', args[1])

    token = kwargs.get('token', args[0])

    user_info = {
        'id': user.id,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'document': user.document,
        'is_active': user.is_active,
        'is_staff': user.is_staff,
        'is_superuser': user.is_superuser,
        'login_type': user.login_type
    }

    # Retornar el token y la info que deseas (Esta debe ser serializable)
    return dict(token=token, user=user_info, permissions=user.get_all_permissions())
