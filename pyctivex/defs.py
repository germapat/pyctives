import importlib
import logging
from rest_framework import status
from rest_framework.response import Response


def validate_permission(permission_type, app_code, permission_code, request):
    if permission_code is not None:
        try:
            permission_name_user = '{}.{}_{}'.format('auth', permission_type, permission_code)
            permission_name_app = '{}.{}_{}'.format(app_code, permission_type, permission_code)

            if permission_code == 'user':
                if not request.user.has_perm(permission_name_user):
                    return Response({'detail': 'Acceso inválido.'}, status=status.HTTP_403_FORBIDDEN)
            elif not request.user.has_perm(permission_name_app):
                return Response({'detail': 'Acceso inválido.'}, status=status.HTTP_403_FORBIDDEN)
        except AttributeError as e:
            logging.exception(e)
            return Response({'detail': 'Acceso inválido.'}, status=status.HTTP_403_FORBIDDEN)
        except Exception as e:
            logging.exception(e)
            return Response({'detail': 'Error inesperado validando permisos.'}, status=status.HTTP_402_PAYMENT_REQUIRED)

    return None


def class_for_name(path: str):
    """
    :param path: str
    :return: django.contrib.admin.ModelAdmin
    """
    module_name, class_name = path.rsplit('.', 1)

    # load the module, will raise ImportError if module cannot be loaded
    m = importlib.import_module(module_name)

    # get the class, will raise AttributeError if class cannot be found
    c = getattr(m, class_name)

    return c
