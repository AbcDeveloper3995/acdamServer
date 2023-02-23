from rest_framework import serializers

from apps.licenciamiento.models import *

#SERIALIZADORES DE LA API SECTOR
class sectorListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre
                }

class sectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'


#SERIALIZADORES DE LA API MUNICIPIO
class municipioListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'nombre': instance['nombre']
                }

class municipioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Municipio
        fields = '__all__'

#SERIALIZADORES DE LA API UTILIZADOR
class utilizadorListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre,
            'tipo': 'Estatal' if instance.tipo == '1' else 'No estatal',
            'fk_sector': instance.fk_sector.nombre,
            'tipoNoEstatal': instance.tipoNoEstatal,
            'tipoDerecho': instance.tipoDerecho,
                }

class utilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        fields = '__all__'

#SERIALIZADORES DE LA API REPRESENTANTE
class representanteListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representante
        fields = '__all__'

    '''
    FUNCION PARA RECORRER TODOS LOS ELEMENTOS DE UN CAMPO MANYTOMANY DE LA INSTANCIA Y ASIGNARLOS A UNA LISTA
    ejemplo: (recorrer todos los municipios que atiende un representante; municipio es el campo MTM) 
    '''
    def recorridoMTM(self, campo):
        aux = []
        for i in campo.all():
            data = {'id': i.id, 'nombre': i.nombre}
            aux.append(data)
        return aux

    def getDescripcionNivelEscolar(self, instance):
        if instance.nivelEscolaridad == '1':
            return 'Tecnico'
        elif instance.nivelEscolaridad == '2':
            return '12 Grado'
        elif instance.nivelEscolaridad == '3':
            return 'Universitario'
        elif instance.nivelEscolaridad == '4':
            return 'Master'
        elif instance.nivelEscolaridad == '5':
            return 'Doctor'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'ci': instance.ci,
            'nombre': instance.nombre,
            'apellidos': instance.apellidos,
            'provincia': instance.provincia,
            'fk_municipio': self.recorridoMTM(instance.fk_municipio),
            'fk_utilizador': self.recorridoMTM(instance.fk_utilizador),
            'fk_sector': self.recorridoMTM(instance.fk_sector),
            'direccion': instance.direccion,
            'nivelEscolaridad': self.getDescripcionNivelEscolar(instance),
            'codigo': instance.codigo,
            'email': instance.email
                }

class representanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representante
        fields = '__all__'

#SERIALIZADORES DE CONTRATO LICENCIA ESTATAL
class contratoLicEstatalListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaEstatal
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fk_utilizador': instance.fk_utilizador.nombre,
                }

class contratoLicenciaEstatalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaEstatal
        fields = '__all__'

    # Funcion que retorna el nombre de la provincia en su formato largo
    def formatoLargoProvincia(self, slug):
        if slug == 'PR':
            return 'Pinar del Rio'
        elif slug == 'ART':
            return 'Artemsia'
        elif slug == 'MAY':
            return 'Mayabeque'
        elif slug == 'HAB':
            return 'La Habanaaaaaa'
        elif slug == 'MAT':
            return 'Matanzas'
        elif slug == 'VCL':
            return 'Villa Clara'
        elif slug == 'CFG':
            return 'Cienfuegos'
        elif slug == 'SS':
            return 'Santi Spiritu'
        elif slug == 'CAV':
            return 'Ciego de Avila'
        elif slug == 'TUN':
            return 'Las Tunas'
        elif slug == 'HOL':
            return 'Holguin'
        elif slug == 'GRM':
            return 'Granma'
        elif slug == 'STG':
            return 'Santiago de Cuba'
        elif slug == 'GTM':
            return 'Guantanamo'
        elif slug == 'IJV':
            return 'Isla de la Juventud'

    def to_representation(self, instance):
        return {
            'titulo': instance.fk_proforma.titulo,
            'descripcion': instance.fk_proforma.descripcion,
            'numeroLicencia': instance.numeroLicencia,
            'codigo': instance.codigo,
            'utilizador': instance.fk_utilizador.nombre,
            'direccion': instance.direccion,
            'provincia': self.formatoLargoProvincia(instance.provincia),
            'municipio': instance.fk_municipio.nombre,
            'nit': instance.nit,
            'fecha': instance.fecha,
            'subordinacion': instance.subordinacion,
            'nombreFirmanteContrato': instance.nombreFirmanteContrato,
            'cargoFirmanteContrato': instance.cargoFirmanteContrato,
            'codigoREEUP': instance.codigoREEUP,
            'cuentaBancaria': instance.cuentaBancaria
                }

#SERIALIZADORES DE PROFORMA
class proformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proforma
        fields = '__all__'

class proformaListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proforma
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'resolucion': instance.resolucion,
            'titulo': instance.titulo,
            'nombre': instance.nombre,
                }

#SERIALIZADORES DE CONTRATO LICENCIA NO ESTATAL PERSONA JURIDICA
class contratoLicenciaPersonaJuridicaListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaPersonaJuridica
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fk_utilizador': instance.fk_utilizador.nombre,
                }

class contratoLicenciaPersonaJuridicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaPersonaJuridica
        fields = '__all__'

    # Funcion que retorna el nombre de la provincia en su formato largo
    def formatoLargoProvincia(self, slug):
        if slug == 'PR':
            return 'Pinar del Rio'
        elif slug == 'ART':
            return 'Artemsia'
        elif slug == 'MAY':
            return 'Mayabeque'
        elif slug == 'HAB':
            return 'La Habanaaaaaa'
        elif slug == 'MAT':
            return 'Matanzas'
        elif slug == 'VCL':
            return 'Villa Clara'
        elif slug == 'CFG':
            return 'Cienfuegos'
        elif slug == 'SS':
            return 'Santi Spiritu'
        elif slug == 'CAV':
            return 'Ciego de Avila'
        elif slug == 'TUN':
            return 'Las Tunas'
        elif slug == 'HOL':
            return 'Holguin'
        elif slug == 'GRM':
            return 'Granma'
        elif slug == 'STG':
            return 'Santiago de Cuba'
        elif slug == 'GTM':
            return 'Guantanamo'
        elif slug == 'IJV':
            return 'Isla de la Juventud'

    def to_representation(self, instance):
        return {
            'titulo': instance.fk_proforma.titulo,
            'descripcion': instance.fk_proforma.descripcion,
            'descripcion2daParte': instance.fk_proforma.descripcion2daParte,
            'descripcion3eraParte': instance.fk_proforma.descripcion3raParte,
            'numeroLicencia': instance.numeroLicencia,
            'codigo': instance.codigo,
            'utilizador': instance.fk_utilizador.nombre,
            'direccion': instance.direccion,
            'provincia': self.formatoLargoProvincia(instance.provincia),
            'municipio': instance.fk_municipio.nombre,
            'nit': instance.nit,
            'fecha': instance.fecha,
            'tipo': instance.tipo,
            'banco': instance.banco,
            'tarifa': instance.tarifa,
            'sucursal': instance.sucursal,
            'nombreFirmanteContrato': instance.nombreFirmanteContrato,
            'cargoFirmanteContrato': instance.cargoFirmanteContrato,
            'codigoOnei': instance.codigoOnei,
            'nombreComercial': instance.nombreComercial,
            'provinciaComercial': instance.provinciaComercial,
            'fk_municipioComercial': instance.fk_municipio.nombre,
            'direccionComercial': instance.direccionComercial,
            'actividadComercial': instance.actividadComercial,
            'email': instance.email,
            'telefono': instance.telefono,
            'ejecucionObrasComercial': instance.ejecucionObrasComercial,
            'representacionObrasEscenicas': instance.representacionObrasEscenicas,
            'comunicacionObrasAudioVisuales': instance.comunicacionObrasAudioVisuales,
                }