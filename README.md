# Directorio Activo
Librería para conectar el directorio activo

## Instalación
Instalar repositorio usando pip. Se debe cambiar USER_NAME por el usuario de bitbucket

    pip install git+https://USER_NAME@bitbucket.org/Emtelco_TIC/pyctivex.git
    
    
### Configuración
Primero se debe realizar la migración de los modelos base de Django para luego registrar la librería pyctivex

    python manage.py migrate
    
### Registro de la librería

Añadir pyctivex en INSTALLED_APPS

```python
INSTALLED_APPS = [
    # django
    ...

    # libraries
    'pyctivex',
]
```



Configurar pyctivex en las configuraciones de Django
****
```python
JWT_AUTH = {
    'JWT_RESPONSE_PAYLOAD_HANDLER': 'pyctivex.authentication.jwt_response_payload_handler',
}

AUTHENTICATION_BACKENDS = [
    'pyctivex.backends.ActiveBackend'
]

AUTH_USER_MODEL = 'pyctivex.User'

 ```
 
 
 
### Registro del modelo custom
 
    python manage.py migrate
    
## Uso del nuevo modelo Usuario

```python
# file app/models.py
from django.contrib.auth import get_user_model

User = get_user_model()


# Example class use
class Example(models.Model):
    user = models.ForeingKey(User)
    
```

### Django urls

```python
    # project/urls.py
    
    from django.urls import path, include
    
    urlpatterns = [
        ...
        path('auth/', include('pyctivex.urls'), namespace='apiauth'))
    ]
    
```

### Soporte para Django import export
Soporte para [django-import-export](https://django-import-export.readthedocs.io/en/latest/)

#### Settings
`USER_IMPORT_EXPORT` por defecto es `False`. Activa la opción de importar y exportar desde el administrador

`USER_RESOURCE_CLASS` por defecto es `import_export.resources.ModelResource`. Se puede usar un recurso propio 

### Configuraciones adicionales

`AUTH_URL` (opcional) Define el url de conexión al directorio activo, por defecto es http://10.1.1.243:8888/ 