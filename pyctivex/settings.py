# -*- coding: utf-8 -*-
from django.conf import settings

LOGIN_LDAP = 'LDAP'
LOGIN_APPLICATION = 'APPLICATION'

LOGIN_TYPE_LIST = [
    (LOGIN_LDAP, 'Directorio activo'),
    (LOGIN_APPLICATION, 'Aplicación')
]

ATTRIBUTE_REQUIRED = '<span style="color: red; font-weight: bold;">*</span>'

USER_RESOURCE_CLASS = getattr(settings, 'USER_RESOURCE_CLASS', 'import_export.resources.ModelResource')

USER_IMPORT_EXPORT = getattr(settings, 'USER_IMPORT_EXPORT', False)
