# -*- coding: utf-8 -*-
from django.contrib import admin, messages
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
from .models import User
from .settings import LOGIN_LDAP, USER_IMPORT_EXPORT
import logging

base_class = ()
attrs = {}

if USER_IMPORT_EXPORT:
    from import_export.admin import ImportExportActionModelAdmin
    from .resources import UserResource

    base_class += (ImportExportActionModelAdmin,)
    attrs['resource_class'] = UserResource


BaseAdmin = type("UserAdmin", base_class, attrs)


@admin.register(User)
class CustomAdmin(UserAdmin, BaseAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (('username', 'document', 'login_type'), 'password1', 'password2'),
        }),
    )

    readonly_fields = ('date_joined', 'last_login')

    def message_user(self, request, message, level=messages.INFO, extra_tags='',
                     fail_silently=False):
        logging.info('on message_user: message: {} | level: {} | extra_tags: {} | fail_silently: {}'
                     .format(message, level, extra_tags, fail_silently))

        message = message.replace(' You may edit it again below.', ' Puedes editarlo abajo')

        super(CustomAdmin, self).message_user(request, format_html(message), level, extra_tags, fail_silently)

    def get_readonly_fields(self, request, obj=None):
        readonly_fields = super(CustomAdmin, self).get_readonly_fields(request, obj) or ()

        if obj and obj.login_type == LOGIN_LDAP:
            readonly_fields += ('first_name', 'last_name', 'email')

        if not request.user.is_superuser:
            readonly_fields += ('is_superuser',)

        return readonly_fields

    def get_fieldsets(self, request, obj=None):
        return super(CustomAdmin, self).get_fieldsets(request, obj)

    def get_queryset(self, request):
        queryset = super(CustomAdmin, self).get_queryset(request)

        if not request.user.is_superuser:
            queryset = queryset.filter(is_superuser=False)
        return queryset

    class Media:
        js = ('pyctivex/js/create-user.js',)
        css = {
            'all': ('pyctivex/css/inputs.css',)
        }
