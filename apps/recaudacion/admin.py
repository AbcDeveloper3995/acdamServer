from django.contrib import admin

from apps.recaudacion.models import *

admin.site.register(Concepto)
admin.site.register(Sucursal)
admin.site.register(Recaudacion)
admin.site.register(Credito)
admin.site.register(ResumenRecaudacionDiaria)
admin.site.register(RecaudacionMensual)
