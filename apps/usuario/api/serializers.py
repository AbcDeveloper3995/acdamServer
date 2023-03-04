from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from apps.usuario.models import *

#SERIALIZADORES DE LA API CARGO
class cargoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.nombre
                }

class cargoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = '__all__'

class customTokenObtainPairSerializer(TokenObtainPairSerializer):
    pass

class customUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('first_name', 'last_name', 'email')

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'nombre': instance.first_name,
            'apellidos': instance.last_name,
            'correo': instance.email,
            'username': instance.username
        }

class usuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'groups', 'password', 'fk_cargo')

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('La contrasena debe tener minimo 8 caracteres')
        return value

    def validate_groups(self, value):
        print(value)
        return value

    # def create(self, validated_data):
    #     usuario = Usuario(**validated_data)
    #     usuario.set_password(validated_data['password'])
    #     usuario.save()
    #     return usuario


class updateUsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('username', 'email', 'first_name', 'last_name')


class usuarioListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario

    def to_representation(self, instance):
        aux = []
        for i in instance.groups.all():
            data = {'id':i.id, 'name':i.name}
            aux.append(data)
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'username': instance.username,
            'email': instance.email,
            'password':instance.password,
            'fk_cargo': instance.fk_cargo.nombre,
            'groups': aux
        }

class grupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'



class grupoListarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'name': instance.name,
        }