from rest_framework import serializers

from apps.licenciamiento.models import *

#SERIALIZADORES DE LA API CARGO
class cargoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'nombre': instance['nombre']
                }

class cargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'


#SERIALIZADORES DE LA API SECTOR
class sectorListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sector
        fields = '__all__'

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'nombre': instance['nombre']
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
            'id': instance['id'],
            'nombre': instance['nombre'],
            'tipo': instance['tipo'],
            'sector': instance['fk_sector__nombre'],
            'tipoNoEstatal': instance['tipoNoEstatal'],
            'tipoDerecho': instance['tipoDerecho'],
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

    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'ci': instance['ci'],
            'nombre': instance['nombre'],
            'apellidos': instance['apellidos'],
            'provincia': instance['provincia'],
            'municipio': instance['fk_municipio__nombre'],
            'utilizador': instance['fk_utilizador__nombre'],
            'sector': instance['fk_sector__nombre'],
            'direccion': instance['direccion'],
            'nivelEscolaridad': instance['nivelEscolaridad'],
            'codigo': instance['codigo'],
            'email': instance['email']
                }

class representanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Representante
        fields = '__all__'