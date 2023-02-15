from django.db import models

from apps.licenciamiento.choices import *

class Base(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False)

    class Meta:
        abstract = True

class ContratoLicenciaBase(models.Model):
    fk_utilizador = models.ForeignKey('Utilizador', verbose_name='Utilizador', blank=True, null=True, on_delete=models.CASCADE)
    fk_representantesAsociados = models.ManyToManyField('Representante', verbose_name='Representantes Asociados', blank=True, null=True)
    fk_municipio = models.ForeignKey('Municipio', verbose_name='Municipio', blank=True, null=True, on_delete=models.CASCADE)
    resolucion = models.CharField(verbose_name='Resolucion', max_length=50, choices=CHOICE_RESOLUCION, blank=False, null=False)
    provincia = models.CharField(verbose_name='Provincia', max_length=50, choices=CHOICE_PROVINCIA, blank=False, null=False)
    fecha = models.DateField(verbose_name='Fecha', auto_now=True)
    numeroLicencia = models.IntegerField(verbose_name='Numero de licencia', blank=False, null=False)
    nit = models.IntegerField(verbose_name='NIT', blank=False, null=False)
    codigo = models.IntegerField(verbose_name='Codigo', blank=False, null=False)
    direccion = models.CharField(verbose_name='Direccion', max_length=150, blank=True)
    estado = models.CharField(verbose_name='Estado', max_length=50, choices=CHOICE_ESTADO, blank=True, null=True)
    tiempoVigencia = models.IntegerField(verbose_name='Tiempo de vigencia', blank=True, null=True)
    fechaVecimiento = models.DateField(verbose_name='Fecha de vencimiento')

    class Meta:
        abstract = True

class Anexo72Base(models.Model):
    fk_contratoLicenciaEstatal= models.ForeignKey('ContratoLicenciaEstatal', verbose_name='Contrato licencia estatal al cual se vincula', blank=True, null=True, on_delete=models.CASCADE)
    periocidadPago = models.CharField(verbose_name='Periocidad de pago', choices=CHOICE_PERIOCIDAD_PAGO, max_length=50, blank=False, null=False)
    periocidadEntrega = models.CharField(verbose_name='Periocidad de entrega', choices=CHOICE_PERIOCIDAD_ENTREGA, max_length=50, blank=False, null=False)

    class Meta:
        abstract = True

class Anexo71Base(models.Model):
    fk_contratoLicenciaPersonaN = models.ForeignKey('ContratoLicenciaPersonaNatural', verbose_name='Contrato licencia persona natural al cual se vincula', blank=True, null=True, on_delete=models.CASCADE)
    fk_contratoLicenciaPersonaJ = models.ForeignKey('ContratoLicenciaPersonaJuridica', verbose_name='Contrato licencia persona juridica al cual se vincula', blank=True, null=True, on_delete=models.CASCADE)
    locacion = models.CharField(verbose_name='Locacion', max_length=150, blank=False, null=False)
    tarifa = models.CharField(verbose_name='Tarifa', max_length=150, blank=False, null=False)
    periocidadPago = models.CharField(verbose_name='Periocidad de pago', choices=CHOICE_PERIOCIDAD_PAGO, max_length=50, blank=False, null=False)

    class Meta:
        abstract = True

class Cargo(Base):
    class Meta:
        db_table = 'Cargo'
        verbose_name = 'Cargos'
        verbose_name_plural = 'Cargo'

    def __str__(self):
        return f'Cargo: {self.nombre}.'

class Resolucion(Base):
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)
    archivo = models.FileField(upload_to='resoluciones', blank=True, null=True)

    class Meta:
        db_table = 'Resolucion'
        verbose_name = 'Resoluciones'
        verbose_name_plural = 'Resoluciones'

    def __str__(self):
        return f'Resolucion: {self.nombre}.'

class Concepto(Base):
    class Meta:
        db_table = 'Concepto'
        verbose_name = 'Conceptos'
        verbose_name_plural = 'Conceptos'

    def __str__(self):
        return f'Concepto: {self.nombre}.'

class Sector(Base):
    class Meta:
        db_table = 'Sector'
        verbose_name = 'Sectores'
        verbose_name_plural = 'Sectores'

    def __str__(self):
        return f'Sector: {self.nombre}.'

class Modalidad(Base):
    class Meta:
        db_table = 'Modalidad'
        verbose_name = 'Modalidades'
        verbose_name_plural = 'Modalidades'

    def __str__(self):
        return f'Modalidad: {self.nombre}.'

class Municipio(Base):
    class Meta:
        db_table = 'Municipio'
        verbose_name = 'Municipios'
        verbose_name_plural = 'Municipios'

    def __str__(self):
        return f'Municipio: {self.nombre}.'

class Utilizador(models.Model):
    fk_sector = models.ForeignKey(Sector, verbose_name='Sector al que pertenece', blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False)
    tipo = models.CharField(verbose_name='Tipo', max_length=50, choices=CHOICE_UTILIZADOR, blank=False, null=False)
    tipoNoEstatal = models.CharField(verbose_name='Tipo de no estatal', choices=CHOICE_UTILIZADOR_NO_ESTATAL, max_length=100, blank=True, null=True)
    tipoDerecho = models.CharField(verbose_name='Tipo de Derecho', max_length=50, choices=CHOICE_DERECHOS, blank=False, null=False)
    esActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Utilizador'
        verbose_name = 'Utilizadores'
        verbose_name_plural = 'Utilizadores'


    def __str__(self):
        return f'Utilizador: {self.nombre} del sector {self.fk_sector.nombre} con derecho {self.tipoDerecho}.'


class Representante(models.Model):
    fk_municipio = models.ManyToManyField(Municipio, verbose_name='Municipio')
    fk_utilizador = models.ManyToManyField(Utilizador, verbose_name='Utilizador')
    fk_sector = models.ManyToManyField(Sector, verbose_name='Sector que atiende')
    provincia = models.CharField(verbose_name='Provincia', max_length=50, choices=CHOICE_PROVINCIA, blank=False, null=False)
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False)
    apellidos = models.CharField(verbose_name='Apellidos', max_length=150, blank=False, null=False)
    ci = models.BigIntegerField(verbose_name='CI', blank=False, null=False)
    direccion = models.CharField(verbose_name='Direccion', max_length=150, blank=False, null=False)
    nivelEscolaridad = models.CharField(verbose_name='Nivel de escolaridad', choices=CHOICE_NIVEL_ESCOLARIDAD, max_length=150, blank=False, null=False)
    codigo = models.IntegerField(verbose_name='Codigo',  blank=False, null=False)
    email = models.CharField(verbose_name='Correo', max_length=50, blank=False, null=False)
    esActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Representante'
        verbose_name = 'Representantes'
        verbose_name_plural = 'Representantes'


    def __str__(self):
        return f'Representante: {self.nombre} {self.apellidos}.'

class ContratoMandatoRepresentante(ContratoLicenciaBase):
    fk_representante = models.ForeignKey(Representante, verbose_name='Representante', related_name="representanteContrato", blank=True, null=True, on_delete=models.CASCADE)
    fk_utilizador = models.ForeignKey(Utilizador, verbose_name='Utilizador', blank=True, null=True, on_delete=models.CASCADE)
    fk_representantesAsociados = models.ManyToManyField('Representante', verbose_name='Representantes Asociados', blank=True, null=True)
    fecha = models.DateField(verbose_name='Fecha', auto_now=True)
    tipoActividad = models.CharField(verbose_name='Tipo de actividad', choices=CHOICE_ACTIVIDAD, max_length=50, blank=False, null=False)
    numeroLicencia = models.IntegerField(verbose_name='Numero de licencia', blank=False, null=False)

    class Meta:
        db_table = 'ContratoMandatoRepresentante'
        verbose_name = 'ContratosMandatoRepresentante'
        verbose_name_plural = 'ContratosMandatoRepresentante'

    def __str__(self):
        return f'Contrato mandato numero {self.numeroLicencia} perteneciente a: {self.fk_representante.nombre} {self.fk_representante.apellidos}.'

class ContratoLicenciaEstatal(ContratoLicenciaBase):
    subordinacion = models.CharField(verbose_name='Subordinacion', max_length=50, blank=False, null=False)
    nombreFirmanteContrato = models.CharField(verbose_name='Nombre de quien firma el contrato', max_length=150, blank=False, null=False)
    cargoFirmanteContrato = models.CharField(verbose_name='Cargo de quien firma el contrato', max_length=150, blank=False, null=False)
    codigoREEUP = models.IntegerField(verbose_name='Codigo REEUP',  blank=False, null=False)
    cuentaBancaria = models.IntegerField(verbose_name='Cuenta Bancaria',  blank=False, null=False)
    emitido = models.BooleanField(default=True)

    class Meta:
        db_table = 'ContratoLicenciaEstatal'
        verbose_name = 'ContratosLicenciaEstatal'
        verbose_name_plural = 'ContratosLicenciaEstatal'

    def __str__(self):
        return f'Contrato licencia estatal numero {self.numeroLicencia} perteneciente a: {self.fk_utilizador.nombre}.'

class ContratoLicenciaPersonaNatural(ContratoLicenciaBase):
    ci = models.BigIntegerField(verbose_name='CI', blank=False, null=False)
    tipoActividad = models.CharField(verbose_name='Tipo de actividad', choices=CHOICE_ACTIVIDAD, max_length=50, blank=False, null=False)
    codigoIdentificadorFiscal = models.IntegerField(verbose_name='Codigo Identificacion fiscal RC50', blank=False, null=False)
    folio = models.IntegerField(verbose_name='Folio', blank=False, null=False)
    cuentaCorriente = models.IntegerField(verbose_name='Cuenta corriente', blank=False, null=False)
    banco = models.CharField(verbose_name='Banco', max_length=150, blank=False, null=False)
    sucursal = models.CharField(verbose_name='Sucursal', max_length=150, blank=False, null=False)
    tarifa = models.IntegerField(verbose_name='Tarifa', blank=False, null=False)

    class Meta:
        db_table = 'ContratoLicenciaPersonaNatural'
        verbose_name = 'ContratosLicenciaPersonaNatural'
        verbose_name_plural = 'ContratosLicenciaPersonaNatural'

    def __str__(self):
        return f'Contrato licencia a persona natural numero {self.numeroLicencia} perteneciente a: {self.fk_utilizador.nombre}.'


class ContratoLicenciaPersonaJuridica(ContratoLicenciaBase):
    fk_municipioComercial = models.ForeignKey(Municipio, verbose_name='Municipio', related_name="municipioComercial", blank=True, null=True, on_delete=models.CASCADE)
    codigoOnei = models.IntegerField(verbose_name='Codigo Onei', blank=False, null=False)
    sucursal = models.CharField(verbose_name='Sucursal', max_length=150, blank=False, null=False)
    cuentaCorriente = models.IntegerField(verbose_name='Cuenta corriente', blank=False, null=False)
    nombreFirmanteContrato = models.CharField(verbose_name='Nombre de quien firma el contrato', max_length=150, blank=False, null=False)
    cargoFirmanteContrato = models.CharField(verbose_name='Cargo de quien firma el contrato', max_length=150, blank=False, null=False)
    emitido = models.BooleanField(default=True)
    nombreComercial = models.CharField(verbose_name='Nombre Comercial', max_length=150, blank=True, null=True)
    direccionComercial = models.CharField(verbose_name='Direccion Comercial', max_length=150, blank=True, null=True)
    provinciaComercial = models.CharField(verbose_name='Provincia Comercial', max_length=150, blank=True, null=True)
    actividadComercial = models.CharField(verbose_name='Actividad Comercial', max_length=150, blank=True, null=True)
    email = models.EmailField(verbose_name='Correo', max_length=150, blank=True, null=True)
    telefono = models.IntegerField(verbose_name='Telefono', blank=True, null=True)
    ejecucionObrasComercial = models.BooleanField(default=False)
    tipoDerechoComercial = models.CharField(verbose_name='Tipo de Derecho Comercial', choices=CHOICE_DERECHOS, max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'ContratoLicenciaPersonaJuridica'
        verbose_name = 'ContratosLicenciaPersonaJuridica'
        verbose_name_plural = 'ContratosLicenciaPersonaJuridica'

    def __str__(self):
        return f'Contrato licencia a persona juridica numero {self.numeroLicencia} perteneciente a: {self.fk_utilizador.nombre}.'


class Anexo72Gaviota(Anexo72Base):
    categoria = models.CharField(verbose_name='Categoria', max_length=150, blank=False, null=False)
    numeroHabitacion = models.IntegerField(verbose_name='Numero Habitacion', blank=False, null=False)
    periodo = models.CharField(verbose_name='Periodo', max_length=150, blank=False, null=False)
    temporadaAlta = models.IntegerField(verbose_name='Temporada alta', blank=False, null=False)
    temporadaBaja = models.IntegerField(verbose_name='Temporada baja', blank=False, null=False)
    ocupacionInferior = models.IntegerField(verbose_name='Ocupacion por debajo del 30%', blank=False, null=False)

    class Meta:
        db_table = 'Anexo72Gaviota'
        verbose_name = 'Anexos72Gaviota'
        verbose_name_plural = 'Anexos72Gaviota'

    def __str__(self):
        return f'Anexo 72 Gaviota vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Anexo72Cimex(Anexo72Base):
    locacion = models.CharField(verbose_name='Locacion', max_length=150, blank=False, null=False)
    modalidad = models.CharField(verbose_name='Modalidad', max_length=150, blank=False, null=False)
    cantidadPlazas = models.IntegerField(verbose_name='Cantidad de plazas', blank=False, null=False)
    tarifa = models.CharField(verbose_name='Tarifa', max_length=150, blank=False, null=False)

    class Meta:
        db_table = 'Anexo72Cimex'
        verbose_name = 'Anexos72Cimex'
        verbose_name_plural = 'Anexos72Cimex'

    def __str__(self):
        return f'Anexo 72 Cimex vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Anexo72TRD(Anexo72Base):
    locacion = models.CharField(verbose_name='Locacion', max_length=150, blank=False, null=False)
    modalidad = models.CharField(verbose_name='Modalidad', max_length=150, blank=False, null=False)
    tarifa = models.CharField(verbose_name='Tarifa', max_length=150, blank=False, null=False)

    class Meta:
        db_table = 'Anexo72TRD'
        verbose_name = 'Anexos72TRD'
        verbose_name_plural = 'Anexos72TRD'

    def __str__(self):
        return f'Anexo 72 TRD vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Anexo71Musica(Anexo71Base):
    tipoMusica = models.CharField(verbose_name='Tipo musica', max_length=150, blank=False, null=False)
    modalidad = models.CharField(verbose_name='Modalidad', max_length=150, blank=False, null=False)
    periocidadEntrega = models.CharField(verbose_name='Periocidad de entrega', choices=CHOICE_PERIOCIDAD_ENTREGA, max_length=50, blank=False, null=False)

    class Meta:
        db_table = 'Anexo71Musica'
        verbose_name = 'Anexos71Musica'
        verbose_name_plural = 'Anexos71Musica'

    def __str__(self):
        return f'Anexo 71 musica vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Anexo71AudioVisual(Anexo71Base):
    categoria = models.CharField(verbose_name='Categoria', max_length=150, blank=False, null=False)
    periocidadEntrega = models.CharField(verbose_name='Periocidad de entrega', default='Mensual', max_length=50, blank=False, null=False)

    class Meta:
        db_table = 'Anexo71AudioVisual'
        verbose_name = 'Anexos71AudioVisual'
        verbose_name_plural = 'Anexos71AudioVisual'

    def __str__(self):
        return f'Anexo 71 audiovisual  vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

