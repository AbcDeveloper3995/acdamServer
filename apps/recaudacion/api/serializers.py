from rest_framework import serializers

from apps.recaudacion.models import *
from apps.utils import formatoLargoProvincia
from apps.validators import validarSoloLetras, validarNoNuloOvacio, validarEntradaNumeroConPunto, \
    validarFechaMenorAfechaActual


# SERIALIZADORES DE LA API CONCEPTO
class conceptoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concepto
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre
        }

class conceptoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Concepto
        fields = '__all__'

    def validate_nombre(self, value):
        sms = 'El campo Nombre solo acepta valores alfabeticos.'
        validarSoloLetras(value, sms)
        return value

# SERIALIZADORES DE LA API SUCURSAL
class sucursalListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'codigo': instance.codigo,
            'fk_municipio': instance.fk_municipio.nombre,
            'provincia': formatoLargoProvincia(instance.provincia),
        }

class sucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = '__all__'


# SERIALIZADORES DE LA API RECAUDACION
class recaudacionListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recaudacion
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fechaCreacion': instance.fechaCreacion,
            'fechaEstadoCuenta': instance.fechaEstadoCuenta,
            'numeroEstadoCuenta': instance.numeroEstadoCuenta,
            'saldoAnterior': instance.saldoAnterior,
            'saldoCierre': instance.saldoCierre,
        }

class recaudacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recaudacion
        fields = '__all__'

    def validate_fechaCreacion(self, value):
        sms = 'El campo Fecha de la recaudacion no puede ser mayor a la fecha actual.'
        validarFechaMenorAfechaActual(value, sms)
        return value

    def validate_saldoAnterior(self, value):
        sms = 'El campo Saldo anterior es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'Entrada no valida en Saldo anterior.'
        validarEntradaNumeroConPunto(str(value), sms)
        return value

    def validate_saldoCierre(self, value):
        sms = 'El campo Saldo cierre es requerido.'
        validarNoNuloOvacio(value, sms)
        sms = 'Entrada no valida en Saldo cierre.'
        validarEntradaNumeroConPunto(str(value), sms)
        return value

# SERIALIZADORES DE LA API CREDITO
class creditoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'
        bancos = {
            1: 'Metropolitano estatal',
            2: 'Metropolitano no estatal',
            3: 'BFI estatal',
            4: 'BFI no estatal',
            5: 'Sociedades',
        }

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fk_utilizador': instance.fk_utilizador.nombre,
            'importe': instance.importe,
            'provincia': instance.provincia,
            'municipio': instance.municipio,
            'transferencia': instance.transferencia,
            'cheque': instance.cheque,
            'factura': instance.factura,
            'devolucion': instance.devolucion,
            'tipoEstatal': self.Meta.bancos.get(instance.tipoEstatal),
        }

class creditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'

# SERIALIZADORES DE LA API RESUMEN RECAUDACION DIARIA
class resumenRecaudacionListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumenRecaudacionDiaria
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fechaCreacion': instance.fechaCreacion.day,
            'totalMetropolitanoEstatal': instance.totalMetropolitanoEstatal,
            'totalMetropolitanoNoEstatal': instance.totalMetropolitanoNoEstatal,
            'totalBfiEstatal': instance.totalBfiEstatal,
            'totalBfiNoEstatal': instance.totalBfiNoEstatal,
            'totalSociedades': instance.totalSociedades,
            'totalGeneral': instance.totalGeneral,
        }

class resumenRecaudacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumenRecaudacionDiaria
        fields = '__all__'

# SERIALIZADORES DE LA API RECAUDACION MENSUAL
class recaudacionMensualListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecaudacionMensual
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'planFronteraEstatal': instance.planFronteraEstatal,
            'realFronteraEstatal': instance.realFronteraEstatal,
            'planFronteraTCP': instance.planFronteraTCP,
            'realFronteraTCP': instance.realFronteraTCP,
            'planSociedad': instance.planSociedad,
            'realSociedad': instance.realSociedad,
            'devolucion': instance.devolucion,
        }

class recaudacionMensualSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecaudacionMensual
        fields = '__all__'

# SERIALIZADORES DE LA API REPORTE COBRO UTILIZADOR
class reporteCobroUtilizadorListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteCobroUtilizador
        fields = '__all__'

    def getChequeOtranfers(self, instance):
        if instance.fk_credito.transferencia == None or instance.fk_credito.transferencia == '':
            return instance.fk_credito.cheque
        return instance.fk_credito.transferencia

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'factura': instance.fk_credito.factura,
            'noReporteFecha': instance.numeroReporteFecha,
            'chequeTransfer': self.getChequeOtranfers(instance),
            'fechaChequeTransfer': instance.fk_credito.fk_recaudacion.fechaEstadoCuenta,
            'cobrado': instance.fk_credito.importe,
            'montoMusicaViva': instance.montoMusicaViva,
            'montoMusicaGrabada': instance.montoMusicaGrabada,
            'montoDerecho': instance.montoDerecho,
            'montoRadio': instance.montoRadio,
            'montoTVmusica': instance.montoTVmusica,
            'montoMora': instance.montoMora,
            'montoTVaudiovisual': instance.montoTVaudiovisual,
            'montoDramatico': instance.montoDramatico,
            'montoCineAudiovisual': instance.montoCineAudiovisual,
            'montoCineDramatico': instance.montoCineDramatico,
            'montoBar': instance.montoBar,
            'montoCafeteria': instance.montoCafeteria,
            'montoRestaurante': instance.montoRestaurante,
            'montoCNocturno': instance.montoCNocturno,
        }

class reporteCobroUtilizadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteCobroUtilizador
        fields = '__all__'