import datetime
import re

from rest_framework import serializers

# FUNCION PARA VALIDAR QUE EL CAMPO NO SEA NULO O VACIO
def validarNoNuloOvacio(value, sms):
    if value == '' or value == None:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR SOLO LETRAS
def validarSoloLetras(value, sms):
    p = re.compile(u"[a-zA-ZñÑáéíóú ]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR SOLO NUMEROS
def validarSoloNumeros(value, sms):
    p = re.compile(u"[0-9]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR SOLO NUMEROS Y LETRAS
def validarSoloNumerosYletras(value, sms):
    p = re.compile(u"[a-zA-ZñÑáéíóú0-9 ]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR SOLO LOS CAMPOS ONEI Y REEUP
def validarEntradaReeupUonei(value, sms):
    p = re.compile(u"[.0-9 ]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR QUE LA LONGITUD SEA IGUAL A UN VALOR
def validarLongitud(value, longitud, sms):
    if str(value).__len__() != longitud:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR QUE LA LONGITUD SEA IGUAL O MENOR A UN VALOR
def validarLongitudMaxima(value, longitud, sms):
    p = re.compile(u"\d+$")
    m = p.match(str(value))
    if str(value).__len__() >= longitud:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR QUE LA FECHA SEA MENOR QUE LA ACTUAL
def validarFechaMenorAfechaActual(value, sms):
    fechaActual = datetime.datetime.today().date()
    if value > fechaActual:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR QUE UN VALOR SEA MAYOR A 0
def validarMayorQue0(value, sms):
    if value < 0:
        raise serializers.ValidationError([sms])
    return value

# FUNCION PARA VALIDAR TARIFAS SOLO EN LOS ANEXOS 71
def validarTarifaAnexos(value, sms):
    p = re.compile(u"[a-zA-ZñÑáéíóú%$0-9 ]+$")
    m = p.match(value)
    if not m:
        raise serializers.ValidationError([sms])
    return value
