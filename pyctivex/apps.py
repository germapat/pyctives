# -*- coding: utf-8 -*-
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class PyCtivexConfig(AppConfig):
    name = 'pyctivex'
    verbose_name = _('User')
    verbose_name_plural = _('Users')
