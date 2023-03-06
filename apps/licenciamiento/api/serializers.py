from rest_framework import serializers

from apps.licenciamiento.models import *
from apps.utils import formatoLargoProvincia

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

#SERIALIZADORES DE LA API MODALIDAD
class modalidadListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre
                }

class modalidadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Modalidad
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

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'titulo': instance.fk_proforma.titulo,
            'encabezado': instance.fk_proforma.encabezado,
            'descripcion': instance.fk_proforma.descripcion,
            'numeroLicencia': instance.numeroLicencia,
            'codigo': instance.codigo,
            'sucursal': instance.sucursal,
            'titular': instance.titular,
            'direccionBanco': instance.direccionBanco,
            'banco': instance.banco,
            'sucursal': instance.sucursal,
            'utilizador': instance.fk_utilizador.nombre,
            'direccion': instance.direccion,
            'provincia': formatoLargoProvincia(instance.provincia),
            'municipio': instance.fk_municipio.nombre,
            'nit': instance.nit,
            'subordinacion': instance.subordinacion,
            'nombreFirmanteContrato': instance.nombreFirmanteContrato,
            'cargoFirmanteContrato': instance.cargoFirmanteContrato,
            'codigoREEUP': instance.codigoREEUP,
            'cuentaBancaria': instance.cuentaBancaria,
            'resolucionUtilizador': instance.resolucionUtilizador,
            'fechaResolucionUtilizador': instance.fechaResolucionUtilizador,
            'emisionResolucionUtilizador': instance.emisionResolucionUtilizador,
            'resolucionFirmante': instance.resolucionFirmante,
            'fechaResolucionFirmante': instance.fechaResolucionFirmante,
            'emitido': instance.emitido,
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
            'tipo': instance.tipo,
                }

#SERIALIZADORES DE CONTRATO LICENCIA NO ESTATAL PERSONA JURIDICA
class contratoLicenciaPersonaJuridicaListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaPersonaJuridica
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fk_utilizador': instance.fk_utilizador.nombre
                }

class contratoLicenciaPersonaJuridicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaPersonaJuridica
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'titulo': instance.fk_proforma.titulo,
            'encabezado': instance.fk_proforma.encabezado,
            'descripcion': instance.fk_proforma.descripcion,
            'descripcion2daParte': instance.fk_proforma.descripcion2daParte,
            'descripcion3eraParte': instance.fk_proforma.descripcion3raParte,
            'numeroLicencia': instance.numeroLicencia,
            'codigo': instance.codigo,
            'utilizador': instance.fk_utilizador.nombre,
            'direccion': instance.direccion,
            'provincia': formatoLargoProvincia(instance.provincia),
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
            'cuentaCorriente': instance.cuentaCorriente,
            'resolucionUtilizador': instance.resolucionUtilizador,
            'fechaResolucionUtilizador': instance.fechaResolucionUtilizador,
            'emisionResolucionUtilizador': instance.emisionResolucionUtilizador,
            'resolucionFirmante': instance.resolucionFirmante,
            'fechaResolucionFirmante': instance.fechaResolucionFirmante,
            'nombreComercial': instance.nombreComercial,
            'provinciaComercial': self.formatoLargoProvincia(instance.provincia),
            'fk_municipioComercial': instance.fk_municipio.nombre,
            'direccionComercial': instance.direccionComercial,
            'actividadComercial': instance.actividadComercial,
            'email': instance.email,
            'telefono': instance.telefono,
            'ejecucionObrasComercial': instance.ejecucionObrasComercial,
            'representacionObrasEscenicas': 'Si' if instance.representacionObrasEscenicas else 'No',
            'comunicacionObrasAudioVisuales': 'Si' if instance.comunicacionObrasAudioVisuales else 'No',
            }

class contratoLicenciaPersonaNaturalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaPersonaNatural
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'titulo': instance.fk_proforma.titulo,
            'encabezado': instance.fk_proforma.encabezado,
            'descripcion': instance.fk_proforma.descripcion,
            'descripcion2daParte': instance.fk_proforma.descripcion2daParte,
            'descripcion3eraParte': instance.fk_proforma.descripcion3raParte,
            'numeroLicencia': instance.numeroLicencia,
            'codigo': instance.codigo,
            'utilizador': instance.fk_utilizador.nombre,
            'direccion': instance.direccion,
            'provincia': formatoLargoProvincia(instance.provincia),
            'municipio': instance.fk_municipio.nombre,
            'nit': instance.nit,
            'fecha': instance.fecha,
            'banco': instance.banco,
            'tarifa': instance.tarifa,
            'sucursal': instance.sucursal,
            'local': instance.local,
            'ci': instance.ci,
            'cuentaCorriente': instance.cuentaCorriente,
            'codigoIdentificadorFiscal': instance.codigoIdentificadorFiscal,
            'folio': instance.folio,
            'nombreComercial': instance.nombreComercial,
            'provinciaComercial': instance.provinciaComercial,
            'fk_municipioComercial': instance.fk_municipio.nombre,
            'direccionComercial': instance.direccionComercial,
            'actividadComercial': 'Gestor de cobro y pago de derecho de autor' if instance.actividadComercial == '1' else 'Cobrador pagador del derecho de autor',
            'email': instance.email,
            'telefono': instance.telefono,
            'ejecucionObrasComercial': instance.ejecucionObrasComercial,
            'representacionObrasEscenicas': 'Si' if instance.representacionObrasEscenicas else 'No',
            'comunicacionObrasAudioVisuales': 'Si' if instance.comunicacionObrasAudioVisuales else 'No',
            }


#SERIALIZADORES DE Anexo71Musica
class anexo71MusicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo71Musica
        fields = '__all__'

class anexo71MusicaListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo71Musica
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_contratoLicenciaEstatal': instance.fk_contratoLicenciaEstatal,
            'fk_contratoLicenciaPersonaJ': instance.fk_contratoLicenciaPersonaJ,
            'locacion': instance.locacion,
            'tarifa': instance.tarifa,
            'periocidadPago': instance.periocidadPago,
            'tipoMusica': instance.tipoMusica,
            'modalidad': instance.modalidad,
            'periocidadEntrega': instance.periocidadEntrega,
                }