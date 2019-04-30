from django.contrib.auth import get_user_model
from django.db import IntegrityError
from import_export import fields
from .settings import USER_RESOURCE_CLASS
from .defs import class_for_name


User = get_user_model()


ParentUserResource = class_for_name(USER_RESOURCE_CLASS)


class UserResource(ParentUserResource):
    document = fields.Field(column_name='Documento', attribute='document')

    login_type = fields.Field(column_name='Tipo de login', attribute='login_type')

    first_name = fields.Field(column_name='Nombre', attribute='first_name')

    last_name = fields.Field(column_name='Apellido', attribute='last_name')

    is_staff = fields.Field(column_name='Es staff', attribute='is_staff', default=False)

    is_active = fields.Field(column_name='Activo', attribute='is_active', default=False)

    last_login = fields.Field(column_name='Último inicio', attribute='last_login', readonly=True)

    date_joined = fields.Field(column_name='Fecha de alta', attribute='date_joined', readonly=True)

    def dehydrate_is_active(self, model) -> str:
        """
        :param model: django.db.models.Model
        :return: str
        """
        return 'si' if model.is_active else 'no'

    dehydrate_is_active.DEFAULT_RESOURCE_FIELD = 'is_active'
    dehydrate_is_active.column_name = 'Activo'

    def dehydrate_is_staff(self, model) -> str:
        """
        :param model: django.db.models.Model
        :return: str
        """
        return 'si' if model.is_staff else 'no'

    dehydrate_is_staff.DEFAULT_RESOURCE_FIELD = 'is_staff'
    dehydrate_is_staff.column_name = 'Es staff'

    def dehydrate_is_superuser(self, model) -> str:
        """
        :param model: django.db.models.Model
        :return: str
        """
        return 'si' if model.is_superuser else 'no'

    dehydrate_is_superuser.DEFAULT_RESOURCE_FIELD = 'is_superuser'

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        try:
            super().save_instance(instance, using_transactions, dry_run)
        except IntegrityError:
            pass

    class Meta:
        model = User
        skip_unchanged = True
        report_skipped = True
        raise_errors = False
        fields = ('id', 'document', 'username', 'is_active', 'login_type', 'is_staff', 'last_login', 'date_joined',
                  'first_name', 'last_name')
        export_order = ('id', 'document', 'username', 'first_name', 'last_name', 'is_active', 'login_type', 'is_staff')
        exclude = ('password',)
