from rest_framework import serializers

from apps.recaudacion.models import *
from apps.utils import formatoLargoProvincia
from apps.validators import validarSoloLetras

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

# SERIALIZADORES DE LA API CREDITO
class creditoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'

    def getDescripcionTipo(self, tipo):
        if tipo == 1:
            return 'Estatal'
        elif tipo == 2:
            return 'No estatal'
        else:
            return 'BFI'

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'fk_utilizador': instance.fk_utilizador.nombre,
            'fk_sucursal': instance.fk_sucursal.codigo,
            'provincia': instance.provincia,
            'municipio': instance.municipio,
            'transferencia': instance.transferencia,
            'cheque': instance.cheque,
            'factura': instance.factura,
            'devolucion': instance.devolucion,
            'tipoEstatal': self.getDescripcionTipo(instance.tipoEstatal),
        }

class creditoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credito
        fields = '__all__'