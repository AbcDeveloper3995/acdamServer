from django.db import models

from apps.licenciamiento.choices import CHOICE_PROVINCIA, CHOICE_CREDITO
from apps.licenciamiento.models import Base, Municipio, Utilizador


class Concepto(Base):
    class Meta:
        db_table = 'Concepto'
        verbose_name = 'Conceptos'
        verbose_name_plural = 'Conceptos'

    def __str__(self):
        return f'Concepto: {self.nombre}.'


class Sucursal(models.Model):
    fk_municipio = models.ForeignKey(Municipio, verbose_name='Municipio', blank=True, null=True,on_delete=models.CASCADE)
    codigo = models.PositiveIntegerField(verbose_name='Codigo', unique=True, blank=True, null=True)
    provincia = models.CharField(verbose_name='Provincia', max_length=50, choices=CHOICE_PROVINCIA, blank=True, null=True)

    class Meta:
        db_table = 'Sucursal'
        verbose_name = 'Sucursal'
        verbose_name_plural = 'Sucursales'

    def __str__(self):
        return f'Sucursal: {str(self.codigo)}'


class Recaudacion(models.Model):
    fechaCreacion = models.DateField(verbose_name='Fecha en que se crea la recaudacion', unique=True, auto_now=True)
    fechaEstadoCuenta = models.DateField(verbose_name='Fecha Estado de Cuenta')
    numeroEstadoCuenta = models.PositiveIntegerField(verbose_name='Numero de estado de cuenta', unique=True, blank=True, null=True)
    saldoAnterior = models.DecimalField(verbose_name='Saldo Anterior', max_digits=11, decimal_places=2, blank=True, null=True)
    saldoCierre = models.DecimalField(verbose_name='Saldo Cierre', max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'Recaudacion'
        verbose_name = 'Recaudacion'
        verbose_name_plural = 'Recaudaciones'

    def __str__(self):
        return f'Recaudacion del: {self.fechaCreacion}'


class Credito(models.Model):
    fk_recaudacion = models.ForeignKey(Recaudacion, verbose_name='Recaudacion', blank=True, null=True, on_delete=models.CASCADE)
    fk_utilizador = models.ForeignKey(Utilizador, verbose_name='Utilizador', blank=True, null=True, on_delete=models.CASCADE)
    fk_sucursal = models.ForeignKey(Sucursal, verbose_name='Sucursal', blank=True, null=True, on_delete=models.CASCADE)
    importe = models.DecimalField(verbose_name='Importe', max_digits=11, decimal_places=2, blank=True, null=True)
    provincia = models.CharField(verbose_name='Provincia', max_length=50, blank=True, null=True)
    municipio = models.CharField(verbose_name='Municipio', max_length=150, blank=True, null=True)
    transferencia = models.CharField(verbose_name='Transferencia', max_length=150, blank=True, null=True)
    cheque = models.CharField(verbose_name='Cheque', max_length=150, blank=True, null=True)
    factura = models.PositiveIntegerField(verbose_name='Factura', blank=True, null=True)
    devolucion = models.DecimalField(verbose_name='Devolucion', max_digits=9, decimal_places=2, blank=True, null=True)
    tipoEstatal = models.PositiveIntegerField(verbose_name='Tipo estatal', choices=CHOICE_CREDITO, blank=False, null=False)
    observacion = models.TextField(verbose_name='Observacion', blank=True, null=True)
    pertenenciaACDAM = models.BooleanField(default=True)

    class Meta:
        db_table = 'Credito'
        verbose_name = 'Credito'
        verbose_name_plural = 'Credito'


    def __str__(self):
        return f'Credito: {self.fk_utilizador.nombre}.'

class ResumenRecaudacionDiaria(models.Model):
    fechaCreacion = models.DateField(verbose_name='Fecha de creacion', unique=True, auto_now=True)
    totalMetropolitanoEstatal = models.DecimalField(verbose_name='Metropolitano estatal', max_digits=11, decimal_places=2, blank=True, null=True)
    totalMetropolitanoNoEstatal = models.DecimalField(verbose_name='Metropolitano no estatal', max_digits=11, decimal_places=2, blank=True, null=True)
    totalBfiEstatal = models.DecimalField(verbose_name='BFI estatal', max_digits=11, decimal_places=2, blank=True, null=True)
    totalBfiNoEstatal = models.DecimalField(verbose_name='BFI no estatal', max_digits=11, decimal_places=2, blank=True, null=True)
    totalSociedades = models.DecimalField(verbose_name='Sociedades', max_digits=11, decimal_places=2, blank=True, null=True)
    totalGeneral = models.DecimalField(verbose_name='General', max_digits=11, decimal_places=2, blank=True, null=True)

    class Meta:
        db_table = 'ResumenRecaudacionDiaria'
        verbose_name = 'ResumenRecaudacionDiaria'
        verbose_name_plural = 'ResumenRecaudacionesDiarias'


    def __str__(self):
        return f'Resumen del dia: {self.fechaCreacion}.'
    
class RecaudacionMensual(models.Model):
    codigo = models.PositiveIntegerField(verbose_name='Codigo', unique=True, blank=True, null=True)
    fronteraEstatal = models.CharField(verbose_name='Frontera Estatal', default='En Frontera Estatal', max_length=50, blank=False, null=False)
    planFronteraEstatal = models.DecimalField(verbose_name='Plan Frontera Estatal', max_digits=11, decimal_places=2, blank=True, null=True)
    realFronteraEstatal = models.DecimalField(verbose_name='Real Frontera Estatal', max_digits=11, decimal_places=2, blank=True, null=True)
    fronteraTCP = models.CharField(verbose_name='Frontera TCP', default='En Frontera TCP', max_length=50, blank=False, null=False)
    planFronteraTCP = models.DecimalField(verbose_name='Plan Frontera TCP', max_digits=11, decimal_places=2, blank=True, null=True)
    realFronteraTCP = models.DecimalField(verbose_name='Real Frontera TCP', max_digits=11, decimal_places=2, blank=True, null=True)
    sociedad = models.CharField(verbose_name='Sociedad', default='En Sociedad', max_length=50, blank=False, null=False)
    planSociedad = models.DecimalField(verbose_name='Plan En Sociedad', max_digits=11, decimal_places=2, blank=True, null=True)
    realSociedad = models.DecimalField(verbose_name='Real En Sociedad', max_digits=11, decimal_places=2, blank=True, null=True)
    devolucion = models.DecimalField(verbose_name='Devolucion', max_digits=11, decimal_places=2, default=0, blank=True, null=True)

    class Meta:
        db_table = 'RecaudacionMensual'
        verbose_name = 'RecaudacionMensual'
        verbose_name_plural = 'RecaudacionMensual'


    def __str__(self):
        return f'Resumen del: {self.codigo}.'