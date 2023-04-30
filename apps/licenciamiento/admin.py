from django.contrib import admin

from apps.licenciamiento.models import *

class utilizadorAdmin(admin.ModelAdmin):
    search_fields = ['nombre']
    list_display = ('id', 'nombre')

admin.site.register(Resolucion)
admin.site.register(Sector)
admin.site.register(Modalidad)
admin.site.register(Municipio)
admin.site.register(Utilizador, utilizadorAdmin)
admin.site.register(Representante)
admin.site.register(ContratoMandatoRepresentante)
admin.site.register(ContratoLicenciaEstatal)
admin.site.register(ContratoLicenciaPersonaNatural)
admin.site.register(ContratoLicenciaPersonaJuridica)
admin.site.register(Anexo72Gaviota)
admin.site.register(Anexo72Cimex)
admin.site.register(Anexo72TRD)
admin.site.register(Anexo71Musica)
admin.site.register(Anexo71AudioVisual)
admin.site.register(Proforma)
admin.site.register(ClasificadorProforma)
admin.site.register(Suplemento)
