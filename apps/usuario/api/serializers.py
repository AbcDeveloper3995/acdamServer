from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.usuario.models import Usuario


class customTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class customUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email')

    def to_representation(self, instance):
        return {
            'nombre': instance.first_name,
            'apellidos': instance.last_name,
            'correo': instance.email,
            'username': instance.username
        }

class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = '__all__'

    def validate_password(self, value):
        print(value)
        if len(value) < 8:
            raise serializers.ValidationError('La contrasena debe tener minimo 8 caracteres')
        return value


    def create(self, validated_data):
        usuario = Usuario(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario


class updateUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name')


class usuarioListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario


    def to_representation(self, instance):
        return {
            'id': instance['id'],
            'Nombre': instance['first_name'],
            'Apellidos': instance['last_name'],
            'Nombre de usuario': instance['username'],
            'Correo': instance['email'],
            'Grupos': instance['groups__name']
        }
