from django.contrib import admin

from .models import Ubicacion
from .models import Datos

admin.site.register(Ubicacion)
admin.site.register(Datos)

# Register your models here.