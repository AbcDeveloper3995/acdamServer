import re

from rest_framework import serializers

# FUNCION PARA VALIDAR SOLO LETRAS
def validarSoloLetras(value):
    p = re.compile(u"[a-zA-ZñÑáéíóú ]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError(['El campo nombre solo admite letras.'])
    return value

# FUNCION PARA VALIDAR SOLO NUMEROS
def validarSoloNumeros(value):
    p = re.compile(u"[0-9]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError(['El campo tal solo admite números.'])
    return value

# FUNCION PARA VALIDAR SOLO NUMEROS Y LETRAS
def validarSoloNumerosYletras(value):
    p = re.compile(u"[a-zA-ZñÑáéíóú0-9 ]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError(['El campo tal solo admite números y letras.'])
    return value

# FUNCION PARA VALIDAR SEL CI
def validarCarnetIdentidad(value):
    p = re.compile(u"\d+$")
    m = p.match(str(value))
    if not m:
        raise serializers.ValidationError(['El campo carnet identidad solo admite números.'])
    if str(value).__len__() != 11:
        raise serializers.ValidationError(['El carné de identidad debe contener 11 dígitos.'])
    return value
