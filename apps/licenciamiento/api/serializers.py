from rest_framework import serializers

from apps.licenciamiento.models import *
from apps.utils import formatoLargoProvincia, getFechaExpiracion, getDescripcionPeriocidadEntrega
from apps.validators import *


# SERIALIZADORES DE LA API SECTOR
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

    def validate_nombre(self, value):
        sms = 'El campo Nombre solo acepta valores alfanumericos.'
        validarSoloLetras(value, sms)
        return value


# SERIALIZADORES DE LA API MODALIDAD
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

    def validate_nombre(self, value):
        sms = 'El campo Nombre solo acepta valores alfanumericos.'
        validarSoloLetras(value, sms)
        return value


# SERIALIZADORES DE LA API MUNICIPIO
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


# SERIALIZADORES DE LA API UTILIZADOR
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
            'tieneContrato': instance.tieneContrato,
        }


class utilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilizador
        fields = '__all__'

    def validate_nombre(self, value):
        sms = 'El campo Nombre solo acepta valores alfanumericos.'
        validarSoloLetras(value, sms)
        return value

    def validate_fk_sector(self, value):
        sms = 'El campo Sector es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_tipoDerecho(self, value):
        sms = 'El campo Tipo derecho es requerido.'
        validarNoNuloOvacio(value, sms)
        return value


# SERIALIZADORES DE LA API REPRESENTANTE
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
            'id': instance.pk,
            'ci': instance.ci,
            'nombre': instance.nombre,
            'apellidos': instance.apellidos,
            'provincia': formatoLargoProvincia(instance.provincia),
            'fk_municipiosAtendidos': self.recorridoMTM(instance.fk_municipiosAtendidos),
            'fk_utilizador': self.recorridoMTM(instance.fk_utilizador),
            'fk_sector': self.recorridoMTM(instance.fk_sector),
            'direccion': instance.direccion,
            'nivelEscolaridad': self.getDescripcionNivelEscolar(instance),
            'codigo': instance.codigo,
            'email': instance.email,
            'tieneContrato': instance.verificarSiTieneContrato()
        }


class representanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representante
        fields = '__all__'

    def validate_nombre(self, value):
        sms = 'El campo Nombre solo acepta valores alfanumericos.'
        validarSoloLetras(value, sms)
        return value

    def validate_ci(self, value):
        sms = 'El campo Carnet identidad de tener 11 digitos.'
        validarLongitud(value, 11, sms)
        sms = 'El campo Carnet identidad debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_apellidos(self, value):
        sms = 'El campo Apellidos solo acepta valores alfanumericos.'
        validarSoloLetras(value, sms)
        return value


# SERIALIZADORES DE CONTRATO LICENCIA ESTATAL
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

    def validate_numeroLicencia(self, value):
        sms = 'El campo numero Licencia debe tener una longitd de hasta 10 caracteres.'
        validarLongitudMaxima(value, 10, sms)
        return value

    def validate_resolucionUtilizador(self, value):
        sms = 'El campo Resolucion utilizador es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Resolucion utilizador solo acepta valores alfanumericos.'
        validarSoloNumerosYletras(value, sms)
        return value

    def validate_fechaResolucionUtilizador(self, value):
        sms = 'El campo Fecha de resolucion utilizador no puede ser mayor a la fecha actual.'
        validarFechaMenorAfechaActual(value, sms)
        return value

    def validate_emisionResolucionUtilizador(self, value):
        sms = 'El campo Resolucion emitida por es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Resolucion emitida por solo acepta valores alfanumericos.'
        validarSoloNumerosYletras(value, sms)
        return value

    def validate_subordinacion(self, value):
        sms = 'El campo Subordinacion solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_fk_municipio(self, value):
        sms = 'El campo Municipio es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_direccion(self, value):
        sms = 'El campo Direccion es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_codigoREEUP(self, value):
        sms = 'Entrada no valida en REEUP.'
        validarEntradaReeupUonei(value, sms)
        sms = 'El campo Codigo REEUP debe tener una longitd de hasta 10 caracteres.'
        validarLongitudMaxima(value, 10, sms)
        return value

    def validate_nit(self, value):
        sms = 'El campo NIT debe tener 11 digitos .'
        validarLongitud(value, 11, sms)
        sms = 'El campo NIT debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_cuentaBancaria(self, value):
        sms = 'El campo Cuenta bancaria debe tener 16 digitos .'
        validarLongitud(value, 16, sms)
        sms = 'El campo Cuenta bancaria debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_titular(self, value):
        if value:
            sms = 'El campo Titular solo acepta valores alfabeticos.'
            validarSoloLetras(value, sms)
        return value

    def validate_banco(self, value):
        sms = 'El campo Banco es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Banco solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    # def validate_sucursal(self, value):
    #     sms = 'El campo Sucursal es requerido.'
    #     validarNoNuloOvacio(value, sms)
    #     sms = 'El campo Sucursal solo acepta valores numericos.'
    #     validarSoloNumeros(value, sms)
    #     return value

    def validate_nombreFirmanteContrato(self, value):
        sms = 'El campo Nombre del firmante solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_cargoFirmanteContrato(self, value):
        sms = 'El campo Cargo del firmante solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_resolucionFirmante(self, value):
        sms = 'El campo Resolucion del firmante solo acepta valores numericos.'
        validarSoloNumeros(value, sms)
        sms = 'El campo Resolucion del firmante es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_fechaResolucionFirmante(self, value):
        sms = 'El campo Fecha de resolucion firmante no puede ser mayor a la fecha actual.'
        validarFechaMenorAfechaActual(value, sms)
        return value

    def validate_emitido(self, value):
        sms = 'El campo Emitido es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Emitido por solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_estado(self, value):
        sms = 'El campo Estado es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_tiempoVigencia(self, value):
        sms = 'El campo Tiempo de vigencia es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fechaCreacionContrato': instance.fechaCreacionContrato,
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
            'estadoVigencia': instance.estadoVigencia,
        }


# SERIALIZADORES DE PROFORMA
class proformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proforma
        fields = '__all__'

    def validate_titulo(self, value):
        sms = 'El campo Titulo es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_encabezado(self, value):
        sms = 'El campo Encabezado es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_tipo(self, value):
        sms = 'El campo Tipo es requerido.'
        validarNoNuloOvacio(value, sms)
        return value


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


# SERIALIZADORES DE CONTRATO LICENCIA NO ESTATAL PERSONA JURIDICA
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

    def validate_numeroLicencia(self, value):
        sms = 'El campo numero Licencia debe tener una longitd de hasta 10 caracteres.'
        validarLongitudMaxima(value, 10, sms)
        return value

    def validate_tipo(self, value):
        sms = 'El campo Tipo es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_resolucionUtilizador(self, value):
        sms = 'El campo Creada mediante es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Creada mediante por solo acepta valores alfanumericos.'
        validarSoloNumerosYletras(value, sms)
        return value

    def validate_fechaResolucionUtilizador(self, value):
        sms = 'El campo Fecha correspondiente a la creacion no puede ser mayor a la fecha actual.'
        validarFechaMenorAfechaActual(value, sms)
        return value

    def validate_direccion(self, value):
        sms = 'El campo Direccion es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_codigoOnei(self, value):
        sms = 'Entrada no valida en Codigo ONEI.'
        validarEntradaReeupUonei(value, sms)
        sms = 'El campo Codigo ONEI debe tener una longitd de hasta 10 caracteres.'
        validarLongitudMaxima(value, 10, sms)
        return value

    def validate_nit(self, value):
        sms = 'El campo NIT debe tener 11 digitos.'
        validarLongitud(value, 11, sms)
        sms = 'El campo NIT debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_cuentaCorriente(self, value):
        sms = 'El campo Cuenta corriente debe tener 16 digitos.'
        validarLongitud(value, 16, sms)
        sms = 'El campo Cuenta corriente debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_nombreFirmanteContrato(self, value):
        sms = 'El campo Nombre del firmante solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_cargoFirmanteContrato(self, value):
        sms = 'El campo Cargo del firmante solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_resolucionFirmante(self, value):
        sms = 'El campo Segun consta es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Segun consta por solo acepta valores alfanumericos.'
        validarSoloNumerosYletras(value, sms)
        return value

    def validate_fechaResolucionFirmante(self, value):
        sms = 'El campo Fecha resolucion firmante no puede ser mayor a la fecha actual.'
        validarFechaMenorAfechaActual(value, sms)
        return value

    def validate_estado(self, value):
        sms = 'El campo Estado es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_tiempoVigencia(self, value):
        sms = 'El campo Tiempo de vigencia es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_banco(self, value):
        sms = 'El campo Banco es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Banco solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    # def validate_sucursal(self, value):
    #     sms = 'El campo Sucursal es requerido.'
    #     validarNoNuloOvacio(value, sms)
    #     sms = 'El campo Sucursal solo acepta valores numericos.'
    #     validarSoloNumeros(value, sms)
    #     return value

    def validate_nombreComercial(self, value):
        if value:
            sms = 'El campo Nombre comercial solo acepta valores alfabeticos.'
            validarSoloLetras(value, sms)
        return value

    def validate_telefono(self, value):
        if value:
            sms = 'El campo telefono debe tener 8 digitos.'
            validarLongitud(value, 8, sms)
        return value

    def getMunicipioComercial(self, instante):
        if not instante.fk_municipioComercial == None:
            return instante.fk_municipioComercial.nombre
        return ''

    def getActividadComercial(self, instante):
        if not instante.fk_modalidad == None:
            return instante.fk_modalidad.nombre
        return ''

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fechaCreacionContrato': instance.fechaCreacionContrato,
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
            'nombreComercial': instance.nombreComercial if instance.nombreComercial != None or instance.nombreComercial != '' else '________',
            'provinciaComercial': formatoLargoProvincia(
                instance.provinciaComercial) if instance.provinciaComercial != None or instance.provinciaComercial != '' else '________',
            'fk_municipioComercial': self.getMunicipioComercial(instance),
            'direccionComercial': instance.direccionComercial,
            'actividadComercial': self.getActividadComercial(instance),
            'email': instance.email,
            'telefono': instance.telefono,
            'ejecucionObrasComercial': instance.ejecucionObrasComercial,
            'representacionObrasEscenicas': 'Si' if instance.representacionObrasEscenicas else 'No',
            'comunicacionObrasAudioVisuales': 'Si' if instance.comunicacionObrasAudioVisuales else 'No',
            'estadoVigencia': instance.estadoVigencia,
        }


# SERIALIZADORES DE CONTRATO LICENCIA NO ESTATAL PERSONA NATURAL
class contratoLicenciaPersonaNaturalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoLicenciaPersonaNatural
        fields = '__all__'

    def validate_numeroLicencia(self, value):
        sms = 'El campo numero Licencia debe tener una longitd de hasta 10 caracteres.'
        validarLongitudMaxima(value, 10, sms)
        return value

    def validate_ci(self, value):
        sms = 'El campo Carnet identidad de tener 11 digitos.'
        validarLongitud(value, 11, sms)
        sms = 'El campo Carnet identidad debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_direccion(self, value):
        sms = 'El campo Direccion es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_fk_modalidad(self, value):
        sms = 'El campo Actividad a ejercer es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_codigoIdentificadorFiscal(self, value):
        sms = 'El campo numero Identificacion FIscal debe tener una longitd de hasta 7 caracteres.'
        validarLongitudMaxima(value, 7, sms)
        return value

    def validate_folio(self, value):
        sms = 'El campo numero Folio debe tener una longitd de hasta 16 caracteres.'
        validarLongitudMaxima(value, 16, sms)
        return value

    def validate_nit(self, value):
        sms = 'El campo NIT debe tener 11 digitos.'
        validarLongitud(value, 11, sms)
        sms = 'El campo NIT debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_cuentaCorriente(self, value):
        sms = 'El campo Cuenta corriente debe tener 16 digitos.'
        validarLongitud(value, 16, sms)
        sms = 'El campo Cuenta corriente debe ser mayor a 0.'
        validarMayorQue0(value, sms)
        return value

    def validate_banco(self, value):
        sms = 'El campo Banco es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'El campo Banco solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

    # def validate_sucursal(self, value):
    #     sms = 'El campo Sucursal es requerido.'
    #     validarNoNuloOvacio(value, sms)
    #     sms = 'El campo Sucursal solo acepta valores numericos.'
    #     validarSoloNumeros(value, sms)
    #     return value

    def validate_estado(self, value):
        sms = 'El campo Estado es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_tiempoVigencia(self, value):
        sms = 'El campo Tiempo de vigencia es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_nombreComercial(self, value):
        if value:
            sms = 'El campo Nombre comercial solo acepta valores alfabeticos.'
            validarSoloLetras(value, sms)
        return value

    def validate_telefono(self, value):
        if value:
            sms = 'El campo Telefono debe tener 8 digitos.'
            validarLongitud(value, 8, sms)
        return value

    def validate_local(self, value):
        if value:
            sms = 'El campo Local solo acepta valores alfabeticos.'
            validarSoloLetras(value, sms)
        return value

    def getMunicipioComercial(self, instante):
        if not instante.fk_municipioComercial == None:
            return instante.fk_municipioComercial.nombre
        return ''

    def getActividadComercial(self, instante):
        if not instante.fk_modalidad == None:
            return instante.fk_modalidad.nombre
        return ''

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fechaCreacionContrato': instance.fechaCreacionContrato,
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
            'banco': instance.banco,
            'tarifa': instance.tarifa,
            'sucursal': instance.sucursal,
            'local': instance.local,
            'ci': instance.ci,
            'cuentaCorriente': instance.cuentaCorriente,
            'codigoIdentificadorFiscal': instance.codigoIdentificadorFiscal,
            'folio': instance.folio,
            'nombreComercial': instance.nombreComercial,
            'provinciaComercial': formatoLargoProvincia(instance.provincia),
            'fk_municipioComercial': self.getMunicipioComercial(instance),
            'direccionComercial': instance.direccionComercial,
            'actividadComercial': self.getActividadComercial(instance),
            'email': instance.email,
            'telefono': instance.telefono,
            'ejecucionObrasComercial': instance.ejecucionObrasComercial,
            'representacionObrasEscenicas': 'Si' if instance.representacionObrasEscenicas else 'No',
            'comunicacionObrasAudioVisuales': 'Si' if instance.comunicacionObrasAudioVisuales else 'No',
            'estadoVigencia': instance.estadoVigencia,
        }


# SERIALIZADORES DE Anexo71Musica
class anexo71MusicaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo71Musica
        fields = '__all__'

    def validate_locacion(self, value):
        sms = 'El campo Locacion solo debe contener valores aflabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_tarifa(self, value):
        sms = 'Tarifa no valida.'
        validarTarifaAnexos(value, sms)
        return value


class anexo71MusicaListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo71Musica
        fields = '__all__'

    def getJuridico(self, instante):
        if not instante.fk_contratoLicenciaPersonaJ == None:
            return instante.fk_contratoLicenciaPersonaJ.id
        return ''

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_contratoLicenciaEstatal': instance.fk_contratoLicenciaEstatal.id,
            'fk_contratoLicenciaPersonaJ': self.getJuridico(instance),
            'locacion': instance.locacion,
            'tarifa': instance.tarifa,
            'periocidadPago': instance.periocidadPago,
            'tipoMusica': instance.tipoMusica,
            'modalidad': instance.modalidad,
            'periocidadEntrega': getDescripcionPeriocidadEntrega(instance.periocidadEntrega)
        }


# SERIALIZADORES DE Anexo71Audiovisual
class anexo71AudiovisualSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo71AudioVisual
        fields = '__all__'

    def validate_locacion(self, value):
        sms = 'El campo Locacion solo debe contener valores aflabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_tarifa(self, value):
        sms = 'Tarifa no valida.'
        validarTarifaAnexos(value, sms)
        return value


class anexo71AudiovisualListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo71AudioVisual
        fields = '__all__'

    def getJuridico(self, instante):
        if not instante.fk_contratoLicenciaPersonaJ == None:
            return instante.fk_contratoLicenciaPersonaJ.id
        return ''

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_contratoLicenciaEstatal': instance.fk_contratoLicenciaEstatal.id,
            'fk_contratoLicenciaPersonaJ': self.getJuridico(instance),
            'locacion': instance.locacion,
            'tarifa': instance.tarifa,
            'periocidadPago': instance.periocidadPago,
            'categoriaAudiovisual': instance.categoriaAudiovisual,
            'periocidadEntrega': getDescripcionPeriocidadEntrega(instance.periocidadEntrega)
        }


# SERIALIZADORES DE Anexo72CIMEX
class anexo72CimexSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo72Cimex
        fields = '__all__'

    def validate_locacionModalidad(self, value):
        sms = 'El campo Locacion solo debe contener valores aflabeticos.'
        validarSoloLetras(value, sms)
        return value

    def validate_tarifa(self, value):
        sms = 'Tarifa no valida.'
        validarSoloNumeros(value, sms)
        return value


class anexo72CimexListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo72Cimex
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_contratoLicenciaEstatal': instance.fk_contratoLicenciaEstatal.id,
            'locacionModalidad': instance.locacionModalidad,
            'tarifa': instance.tarifa,
            'periocidadPago': instance.periocidadPago,
            'cantidadPlazas': instance.cantidadPlazas,
            'importe': instance.importe,
            'periocidadEntrega': getDescripcionPeriocidadEntrega(instance.periocidadEntrega)
        }


# SERIALIZADORES DE Anexo72Gaviota
class anexo72GaviotaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo72Gaviota
        fields = '__all__'

    def validate_periodo(self, value):
        sms = 'El campo Periodo solo acepta valores alfanumericos.'
        validarSoloNumerosYletras(value, sms)
        return value

    def validate_tarifa(self, value):
        sms = 'Tarifa no valida.'
        validarSoloNumeros(value, sms)
        return value


class anexo72GaviotaListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo72Gaviota
        fields = '__all__'

    def getFormatoCategorias(self, categoria):
        if categoria == '2estrellas':
            return '2 Estrellas'
        if categoria == '3estrellas':
            return '3 Estrellas'
        if categoria == '4estrellas':
            return '4 Estrellas'
        if categoria == '5estrellas':
            return '5 Estrellas'

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_contratoLicenciaEstatal': instance.fk_contratoLicenciaEstatal.id,
            'categoria': self.getFormatoCategorias(instance.categoria),
            'numeroHabitacion': instance.numeroHabitacion,
            'periodo': instance.periodo,
            'periocidadPago': instance.periocidadPago,
            'tarifaTemporadaAlta': instance.tarifaTemporadaAlta,
            'tarifaTemporadaBaja': instance.tarifaTemporadaBaja,
            'tarifaOcupacionInferior': instance.tarifaOcupacionInferior,
            'importeTemporadaAlta': instance.importeTemporadaAlta,
            'importeTemporadaBaja': instance.importeTemporadaBaja,
            'importeTemporadaOcupacionInferior': instance.importeTemporadaOcupacionInferior,
            'periocidadEntrega': getDescripcionPeriocidadEntrega(instance.periocidadEntrega),
        }


# SERIALIZADORES DE Anexo72TRD
class anexo72TrdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo72TRD
        fields = '__all__'

    def validate_locacion(self, value):
        sms = 'El campo Locacion solo debe contener valores aflabeticos.'
        validarSoloLetras(value, sms)
        return value


class anexo72TrdListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Anexo72TRD
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_contratoLicenciaEstatal': instance.fk_contratoLicenciaEstatal.id,
            'locacion': instance.locacion,
            'tarifa': instance.tarifa,
            'periocidadPago': instance.periocidadPago,
            'importe': instance.importe,
            'modalidad': instance.modalidad,
            'periocidadEntrega': getDescripcionPeriocidadEntrega(instance.periocidadEntrega),
        }


# SERIALIZADORES DE CONTRATO MANDATO
class contratoMandatoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoMandatoRepresentante
        fields = '__all__'

    def validate_remuneracion(self, value):
        sms = 'El campo remuneracion es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_numeroContrato(self, value):
        sms = 'El campo numero de contrato es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_fechaInscripcion(self, value):
        sms = 'El campo fecha de inscripcion no puede ser mayor a la fecha actual.'
        validarFechaMenorAfechaActual(value, sms)
        return value

    def validate_fechaLicencia(self, value):
        sms = 'El campo fecha de licencia no puede ser mayor a la fecha actual.'
        validarFechaMenorAfechaActual(value, sms)
        return value


class contratoMandatoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContratoMandatoRepresentante
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_representante': instance.fk_representante.getNombreCompleto(),
            'ci': instance.fk_representante.ci,
            'direccion': instance.fk_representante.direccion,
            'municipioResidente': instance.fk_representante.fk_municipioResidente.nombre,
            'provincia': formatoLargoProvincia(instance.fk_representante.provincia),
            'fechaCreacion': instance.fechaCreacion,
            'tipoActividad': 'Gestor de cobro y pago de derecho de autor' if instance.tipoActividad == '1' else 'Cobrador pagador del derecho de autor',
            'numeroContrato': instance.numeroContrato,
            'numeroLicencia': instance.numeroLicencia,
            'fechaLicencia': instance.fechaLicencia,
            'fechaInscripcion': instance.fechaInscripcion,
            'remuneracion': instance.remuneracion,
            'titulo': instance.fk_proforma.titulo,
            'encabezado': instance.fk_proforma.encabezado,
            'descripcion': instance.fk_proforma.descripcion,
            'descripcion2daParte': instance.fk_proforma.descripcion2daParte,
        }


# SERIALIZADORES DE CLASIFICADOR PROFORMA
class clasificadorProformaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasificadorProforma
        fields = '__all__'

    def validate_fk_proforma(self, value):
        sms = 'El campo Proforma es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_fk_sector(self, value):
        sms = 'El campo Sector es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_tipo(self, value):
        sms = 'El campo Tipo es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_tipoDerecho(self, value):
        sms = 'El campo Derecho es requerido.'
        validarNoNuloOvacio(value, sms)
        return value


class clasificadorProformaListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClasificadorProforma
        fields = '__all__'

    def getSector(self, instance):
        if not instance.fk_sector == None:
            return instance.fk_sector.nombre
        return ''

    def getTipoDerecho(self, instance):
        if not instance.tipoDerecho == None:
            return instance.tipoDerecho
        return ''

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'fk_proforma': instance.fk_proforma.nombre,
            'fk_sector': self.getSector(instance),
            'tipo': 'Estatal' if instance.tipo == '1' else 'No estatal',
            'tipoDerecho': self.getTipoDerecho(instance),
        }


# SERIALIZADORES DE SUPLEMENTO
class suplementoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suplemento
        fields = '__all__'

    def validate_titulo(self, value):
        sms = 'El campo Titulo es requerido.'
        validarNoNuloOvacio(value, sms)
        return value

    def validate_cuentaBancaria(self, value):
        if value != None:
            sms = 'El campo Cuenta corriente debe tener 16 digitos.'
            validarLongitud(value, 16, sms)
            sms = 'El campo Cuenta corriente debe ser mayor a 0.'
            validarMayorQue0(value, sms)
            return value
        return value

    def validate_nombreFirmanteContrato(self, value):
        if value:
            sms = 'El campo Nombre del firmante solo acepta valores alfabeticos.'
            validarSoloLetras(value, sms)
            return value
        return ''

    def validate_cargoFirmanteContrato(self, value):
        if value:
            sms = 'El campo Cargo del firmante solo acepta valores alfabeticos.'
            validarSoloLetras(value, sms)
            return value
        return ''

    def validate_resolucionFirmante(self, value):
        if value:
            sms = 'El campo Segun consta es requerido.'
            validarNoNuloOvacio(value, sms)
            sms = 'El campo Segun consta por solo acepta valores alfanumericos.'
            validarSoloNumerosYletras(value, sms)
            return value
        return ''

    def validate_fechaResolucionFirmante(self, value):
        if value:
            sms = 'El campo Fecha resolucion firmante no puede ser mayor a la fecha actual.'
            validarFechaMenorAfechaActual(value, sms)
            return value
        return value


class suplementoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suplemento
        fields = '__all__'

    ''' Este conjunto de funciones es para ir formando la descripcion que se va a retornar como descripcionUtilizador;
    si algunos de los campos es cambiado al crear el suplemento, ejemplo se cambio la cuenta bancaria entonces la funcion correspondiente
    (getCuentaBancaria) retornara la cuenta que se ingreso al crear el suplemento, sino retornara la cuenta bancaria que tenga el contrato y
    sera en funcion de la (fk) que llegue ya sea Estatal, No estatal juridico o No estatal personal
    '''

    def getEncabezadoSegunContrato(self, instance):
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.fk_proforma.encabezado
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.fk_proforma.encabezado
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return instance.fk_contratoLicenciaPersonaNatural.fk_proforma.encabezado

    def getCuentaBancaria(self, instance):
        if instance.cuentaBancaria != '' and instance.cuentaBancaria != None:
            return instance.cuentaBancaria
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.cuentaBancaria
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.cuentaCorriente
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return instance.fk_contratoLicenciaPersonaNatural.cuentaCorriente

    def getDireccion(self, instance):
        if instance.direccion != '' and instance.direccion != None:
            return instance.direccion
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.direccion
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.direccion
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return instance.fk_contratoLicenciaPersonaNatural.direccion

    def getSucursal(self, instance):
        if instance.sucursal != '' and instance.sucursal != None:
            return instance.sucursal
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.sucursal
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.sucursal
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return instance.fk_contratoLicenciaPersonaNatural.sucursal

    def getNombreFirmante(self, instance):
        if instance.nombreFirmanteContrato != '' and instance.nombreFirmanteContrato != None:
            return instance.nombreFirmanteContrato
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.nombreFirmanteContrato
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.nombreFirmanteContrato
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return instance.fk_contratoLicenciaPersonaNatural.fk_utilizador.nombre

    def getCargoFirmante(self, instance):
        if instance.cargoFirmanteContrato != '' and instance.cargoFirmanteContrato != None:
            return instance.cargoFirmanteContrato
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.cargoFirmanteContrato
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.cargoFirmanteContrato
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return ''

    def getResolucionFirmante(self, instance):
        if instance.resolucionFirmante != '' and instance.resolucionFirmante != None:
            return instance.resolucionFirmante
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.resolucionFirmante
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.resolucionFirmante
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return instance.fk_contratoLicenciaPersonaNatural.resolucionFirmante

    def getFechaResolucionFirmante(self, instance):
        fecha = instance.fechaResolucionFirmante
        if instance.fechaResolucionFirmante != '' and instance.fechaResolucionFirmante != None:
            return fecha
        if not instance.fk_contratoLicenciaEstatal == None:
            return instance.fk_contratoLicenciaEstatal.fechaResolucionFirmante
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            return instance.fk_contratoLicenciaPersonaJuridica.fechaResolucionFirmante
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            return instance.fk_contratoLicenciaPersonaNatural.fechaResolucionFirmante

    ''' Aca se va a retornar una descripcion en dependencia de la (fk) que llegue, ya sea (Estatal, No estatal Juridico, No estatal Natural) 
        '''

    def getDescripcionUtilizador(self, instance):
        if not instance.fk_contratoLicenciaEstatal == None:
            descripcion = f'DE OTRA PARTE: {instance.fk_contratoLicenciaEstatal.fk_utilizador.nombre}, con domicilio legal en ' \
                          f'{self.getDireccion(instance)}, el la provincia {instance.fk_contratoLicenciaEstatal.provincia},' \
                          f' municipio {instance.fk_contratoLicenciaEstatal.fk_municipio.nombre}, con Codigo REEUP: {instance.fk_contratoLicenciaEstatal.codigoREEUP}, NIT: ' \
                          f'{instance.fk_contratoLicenciaEstatal.nit}, Cuenta Bancaria en CUP No {self.getCuentaBancaria(instance)}, ' \
                          f'en el Banco de Credito y Comercio {instance.fk_contratoLicenciaEstatal.banco}, Sucursal ' \
                          f'{self.getSucursal(instance)}, que en lo adelante se le denominara, a los efectos de este contrato, UTILIZADOR, ' \
                          f'representado en este acto por {self.getNombreFirmante(instance)}, en su caracter de ' \
                          f'{self.getCargoFirmante(instance)}, designado en este cargo por la Resolucion ' \
                          f'{self.getResolucionFirmante(instance)}, de fecha {self.getFechaResolucionFirmante(instance)}, ' \
                          f'emitida por {instance.fk_contratoLicenciaEstatal.emitido}.'

            return descripcion
        if not instance.fk_contratoLicenciaPersonaJuridica == None:
            descripcion = f'DE OTRA PARTE: {instance.fk_contratoLicenciaPersonaJuridica.fk_utilizador.nombre}, con domicilio legal en ' \
                          f'{self.getDireccion(instance)}, el la provincia {instance.fk_contratoLicenciaPersonaJuridica.provincia},' \
                          f' municipio {instance.fk_contratoLicenciaPersonaJuridica.fk_municipio.nombre}, con Codigo ONEI: {instance.fk_contratoLicenciaPersonaJuridica.codigoOnei}, NIT: ' \
                          f'{instance.fk_contratoLicenciaPersonaJuridica.nit}, Cuenta Bancaria en CUP No {self.getCuentaBancaria(instance)}, ' \
                          f'en el Banco de Credito y Comercio {instance.fk_contratoLicenciaPersonaJuridica.banco}, Sucursal ' \
                          f'{self.getSucursal(instance)}, que en lo adelante se le denominara, a los efectos de este contrato, UTILIZADOR, ' \
                          f'representado en este acto por {self.getNombreFirmante(instance)}, en su caracter de ' \
                          f'{self.getCargoFirmante(instance)}, designado en este cargo por la Resolucion ' \
                          f'{self.getResolucionFirmante(instance)}, de fecha {self.getFechaResolucionFirmante(instance)}, ' \
                          f'emitida por {instance.fk_contratoLicenciaPersonaJuridica.emitido}.'

            return descripcion
        if not instance.fk_contratoLicenciaPersonaNatural == None:
            descripcion = f'DE OTRA PARTE: El trabajador por cuenta propia {instance.fk_contratoLicenciaPersonaNatural.fk_utilizador.nombre}, ' \
                          f'con numero de identidad permanente {instance.fk_contratoLicenciaPersonaNatural.ci} con domicilio legal en ' \
                          f'{self.getDireccion(instance)}, el la provincia {instance.fk_contratoLicenciaPersonaNatural.provincia},' \
                          f' municipio {instance.fk_contratoLicenciaPersonaNatural.fk_municipio.nombre}, autorizador a ejercer el trabajo por cuenta ' \
                          f'propia en la actividad {instance.fk_contratoLicenciaPersonaNatural.fk_modalidad.nombre}, con identificacion Fiscal Unica ' \
                          f'RC - 05, con numeracion {instance.fk_contratoLicenciaPersonaNatural.codigoIdentificadorFiscal}, NIT: ' \
                          f'{instance.fk_contratoLicenciaPersonaNatural.nit}, Cuenta Bancaria en CUP No {self.getCuentaBancaria(instance)}, ' \
                          f'en el Banco de Credito y Comercio {instance.fk_contratoLicenciaPersonaNatural.banco}, Sucursal ' \
                          f'{self.getSucursal(instance)}, que en lo adelante se le denominara, a los efectos de este contrato, UTILIZADOR.'
            return descripcion

    def to_representation(self, instance):
        return {
            'id': instance.pk,
            'titulo': instance.titulo,
            'encabezado': self.getEncabezadoSegunContrato(instance),
            'utilizador': self.getDescripcionUtilizador(instance),
            'descripcion': instance.descripcion,
            'cargoFirmanteSuplemento': self.getCargoFirmante(instance),
            'firmanteSuplemento': self.getNombreFirmante(instance),
        }
