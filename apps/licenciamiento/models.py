from django.db import models

from apps.licenciamiento.choices import *
from apps.usuario.models import Usuario
from apps.licenciamiento.choices import *
from apps.usuario.models import Usuario

class Base(models.Model):
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False)

    class Meta:
        abstract = True

class ContratoLicenciaBase(models.Model):
    fk_usuario = models.ForeignKey(Usuario, verbose_name='Creado por', blank=True, null=True,on_delete=models.CASCADE)
    fk_proforma = models.ForeignKey('Proforma', verbose_name='Proforma', blank=True, null=True, on_delete=models.CASCADE)
    fk_utilizador = models.ForeignKey('Utilizador', verbose_name='Utilizador', blank=True, null=True, on_delete=models.CASCADE)
    fk_representantesAsociados = models.ManyToManyField('Representante', verbose_name='Representantes Asociados', blank=True, null=True)
    fk_municipio = models.ForeignKey('Municipio', verbose_name='Municipio', blank=True, null=True, on_delete=models.CASCADE)
    banco = models.CharField(verbose_name='Banco', default='BANDEC', max_length=150, blank=True, null=True)
    sucursal = models.CharField(verbose_name='Sucursal', max_length=150, blank=True, null=True)
    titular = models.CharField(verbose_name='Titular de la cuenta', max_length=250, blank=True, null=True)
    direccionBanco = models.CharField(verbose_name='Direccion del Banco', max_length=250, blank=True, null=True)
    provincia = models.CharField(verbose_name='Provincia', max_length=50, choices=CHOICE_PROVINCIA, blank=False, null=False)
    fechaCreacionContrato = models.DateField(verbose_name='Fecha en que se crea el contrato', auto_now=True)
    numeroLicencia = models.PositiveIntegerField(verbose_name='Numero de licencia', unique=True, blank=False, null=False)
    nit = models.BigIntegerField(verbose_name='NIT', unique=True, blank=True, null=True)
    codigo = models.PositiveIntegerField(verbose_name='Codigo', unique=True, blank=False, null=False)
    direccion = models.CharField(verbose_name='Direccion', max_length=150, blank=True)
    estado = models.CharField(verbose_name='Estado', max_length=50, choices=CHOICE_ESTADO, blank=True, null=True)
    tiempoVigencia = models.PositiveIntegerField(verbose_name='Tiempo de vigencia', blank=True, null=True)
    fechaVecimiento = models.DateField(verbose_name='Fecha de vencimiento', blank=True, null=True)
    estadoVigencia = models.IntegerField(verbose_name='Estado de vigencia', default=1, choices=CHOICE_VIGENCIA, blank=True, null=True)

    class Meta:
        abstract = True

class Anexo72Base(models.Model):
    fk_contratoLicenciaEstatal = models.ForeignKey('ContratoLicenciaEstatal', verbose_name='Contrato licencia estatal al cual se vincula', blank=True, null=True, on_delete=models.CASCADE)
    periocidadPago = models.CharField(verbose_name='Periocidad de pago', choices=CHOICE_PERIOCIDAD_PAGO, max_length=50, blank=True, null=True)
    periocidadEntrega = models.CharField(verbose_name='Periocidad de entrega', choices=CHOICE_PERIOCIDAD_ENTREGA, max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

class Anexo71Base(models.Model):
    fk_contratoLicenciaEstatal = models.ForeignKey('ContratoLicenciaEstatal',
                                                   verbose_name='Contrato licencia estatal al cual se vincula',
                                                   blank=True, null=True, on_delete=models.CASCADE)
    fk_contratoLicenciaPersonaJ = models.ForeignKey('ContratoLicenciaPersonaJuridica', verbose_name='Contrato licencia persona juridica al cual se vincula', blank=True, null=True, on_delete=models.CASCADE)
    locacion = models.CharField(verbose_name='Locacion', max_length=150, blank=False, null=False)
    tarifa = models.CharField(verbose_name='Tarifa', max_length=150, blank=False, null=False)
    periocidadPago = models.CharField(verbose_name='Periocidad de pago', choices=CHOICE_PERIOCIDAD_PAGO, max_length=50, blank=True, null=True)

    class Meta:
        abstract = True

class Resolucion(Base):
    descripcion = models.CharField(verbose_name='Descripcion', max_length=200, blank=True, null=True)
    archivo = models.FileField(upload_to='resoluciones', blank=True, null=True)

    class Meta:
        db_table = 'Resolucion'
        verbose_name = 'Resoluciones'
        verbose_name_plural = 'Resoluciones'

    def __str__(self):
        return f'Resolucion: {self.nombre}.'


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
    codigo = models.PositiveIntegerField(verbose_name='Codigo', blank=True, null=True)

    class Meta:
        db_table = 'Municipio'
        verbose_name = 'Municipios'
        verbose_name_plural = 'Municipios'

    def __str__(self):
        return f'Municipio: {self.nombre}.'

class Utilizador(models.Model):
    fk_sector = models.ForeignKey(Sector, verbose_name='Sector al que pertenece', blank=True, null=True, on_delete=models.CASCADE)
    nombre = models.CharField(verbose_name='Nombre', max_length=250, blank=False, null=False)
    tipo = models.CharField(verbose_name='Tipo', max_length=50, choices=CHOICE_UTILIZADOR, blank=False, null=False)
    tipoNoEstatal = models.CharField(verbose_name='Tipo de no estatal', choices=CHOICE_UTILIZADOR_NO_ESTATAL, max_length=100, blank=True, null=True)
    tipoDerecho = models.CharField(verbose_name='Tipo de Derecho', max_length=50, choices=CHOICE_DERECHOS, blank=False, null=False)
    tieneContrato = models.BooleanField(default=False)
    esActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Utilizador'
        verbose_name = 'Utilizadores'
        verbose_name_plural = 'Utilizadores'

    def __str__(self):
        return f'Utilizador: {self.nombre} del sector {self.fk_sector.nombre} con derecho {self.tipoDerecho}.'


class Representante(models.Model):
    fk_municipiosAtendidos = models.ManyToManyField(Municipio, verbose_name='Municipios que atiende')
    fk_municipioResidente = models.ForeignKey(Municipio, verbose_name='Municipio donde reside', related_name="municipioResidente", blank=True, null=True,on_delete=models.CASCADE)
    fk_utilizador = models.ManyToManyField(Utilizador, verbose_name='Utilizador')
    fk_sector = models.ManyToManyField(Sector, verbose_name='Sector que atiende')
    fk_usuario = models.ForeignKey(Usuario, verbose_name='Atendido por', blank=True, null=True, on_delete=models.CASCADE)
    provincia = models.CharField(verbose_name='Provincia', max_length=50, choices=CHOICE_PROVINCIA, blank=False, null=False)
    nombre = models.CharField(verbose_name='Nombre', max_length=50, blank=False, null=False)
    apellidos = models.CharField(verbose_name='Apellidos', max_length=150, blank=False, null=False)
    ci = models.BigIntegerField(verbose_name='CI', unique=True, blank=False, null=False)
    direccion = models.CharField(verbose_name='Direccion', max_length=150, blank=False, null=False)
    nivelEscolaridad = models.CharField(verbose_name='Nivel de escolaridad', choices=CHOICE_NIVEL_ESCOLARIDAD, max_length=150, blank=False, null=False)
    codigo = models.CharField(verbose_name='Codigo', max_length=5, blank=False, null=False)
    email = models.EmailField(verbose_name='Correo', max_length=50, blank=True, null=True)
    esActivo = models.BooleanField(default=True)

    class Meta:
        db_table = 'Representante'
        verbose_name = 'Representantes'
        verbose_name_plural = 'Representantes'


    def __str__(self):
        return f'Representante: {self.nombre} {self.apellidos}.'

    def getNombreCompleto(self):
        return f'{self.nombre} {self.apellidos}'

    def verificarSiTieneContrato(self):
        tieneContrato = False
        query = ContratoMandatoRepresentante.objects.filter(fk_representante__pk=self.pk)
        if query.exists():
            tieneContrato = True
        return tieneContrato

class ContratoMandatoRepresentante(models.Model):
    fk_usuario = models.ForeignKey(Usuario, verbose_name='Creado por', blank=True, null=True, on_delete=models.CASCADE)
    fk_proforma = models.ForeignKey('Proforma', verbose_name='Proforma', blank=True, null=True, on_delete=models.CASCADE)
    fk_representante = models.ForeignKey(Representante, verbose_name='Representante', related_name="representanteContrato", blank=True, null=True, on_delete=models.CASCADE)
    fk_utilizador = models.ForeignKey(Utilizador, verbose_name='Utilizador', blank=True, null=True, on_delete=models.CASCADE)
    fk_representantesAsociados = models.ManyToManyField('Representante', verbose_name='Representantes Asociados', blank=True, null=True)
    fechaCreacion = models.DateField(verbose_name='Fecha creacion del contrato', auto_now=True)
    fechaLicencia = models.DateField(verbose_name='Fecha de Licencia', blank=True, null=True)
    fechaInscripcion = models.DateField(verbose_name='Fecha de Inscripcion', blank=True, null=True)
    tipoActividad = models.CharField(verbose_name='Tipo de actividad', choices=CHOICE_ACTIVIDAD, max_length=50, blank=False, null=False)
    numeroLicencia = models.PositiveIntegerField(verbose_name='Numero de licencia', unique=True, blank=True, null=True)
    numeroContrato = models.PositiveIntegerField(verbose_name='Numero de Contrato', unique=True, blank=True, null=True)
    remuneracion = models.DecimalField(verbose_name='Remuneracion estatal', max_digits=7, decimal_places=2, blank=True, null=True)
    remuneracionNoEstatal = models.IntegerField(verbose_name='Remuneracion no estatal', blank=True, null=True)

    class Meta:
        db_table = 'ContratoMandatoRepresentante'
        verbose_name = 'ContratosMandatoRepresentante'
        verbose_name_plural = 'ContratosMandatoRepresentante'

    def __str__(self):
        return f'Contrato mandato numero {self.numeroLicencia} perteneciente a: {self.fk_representante.nombre} {self.fk_representante.apellidos}.'

class ContratoLicenciaEstatal(ContratoLicenciaBase):
    resolucionUtilizador = models.CharField(verbose_name='Resolucion Utilizador', max_length=200, blank=True, null=True)
    fechaResolucionUtilizador = models.DateField(verbose_name='Fecha resolucion Utilizador', blank=True, null=True)
    emisionResolucionUtilizador = models.CharField(verbose_name='Resolucion utilizador (emitida/creda por)',
                                                   max_length=150, blank=True, null=True)
    resolucionFirmante = models.CharField(verbose_name='Resolucion del firmante', max_length=200, blank=True, null=True)
    fechaResolucionFirmante = models.DateField(verbose_name='Fecha resolucion firmante', blank=True, null=True)
    subordinacion = models.CharField(verbose_name='Subordinacion', max_length=50, blank=False, null=False)
    nombreFirmanteContrato = models.CharField(verbose_name='Nombre de quien firma el contrato', max_length=150, blank=False, null=False)
    cargoFirmanteContrato = models.CharField(verbose_name='Cargo de quien firma el contrato', max_length=150, blank=False, null=False)
    codigoREEUP = models.CharField(verbose_name='Codigo REEUP',  max_length=150, unique=True, blank=True, null=True)
    cuentaBancaria = models.BigIntegerField(verbose_name='Cuenta Bancaria',  unique=True, blank=False, null=False)
    emitido = models.CharField(verbose_name='Emitido por', max_length=250, blank=True, null=True)

    class Meta:
        db_table = 'ContratoLicenciaEstatal'
        verbose_name = 'ContratosLicenciaEstatal'
        verbose_name_plural = 'ContratosLicenciaEstatal'

    def __str__(self):
        return f'Contrato licencia estatal numero {self.numeroLicencia} perteneciente a: {self.fk_utilizador.nombre}.'

class ContratoLicenciaPersonaNatural(ContratoLicenciaBase):
    fk_modalidad = models.ForeignKey(Modalidad, verbose_name='Actividad Comercial', blank=True, null=True, on_delete=models.CASCADE)
    fk_municipioComercial = models.ForeignKey(Municipio, verbose_name='Municipio Comercial', related_name="municipioComercialPN",
                                              blank=True, null=True, on_delete=models.CASCADE)
    ci = models.BigIntegerField(verbose_name='CI', unique=True, blank=False, null=False)
    codigoIdentificadorFiscal = models.PositiveIntegerField(verbose_name='Codigo Identificacion fiscal RC50', unique=True, blank=False, null=False)
    folio = models.PositiveIntegerField(verbose_name='Folio', unique=True, blank=False, null=False)
    cuentaCorriente = models.BigIntegerField(verbose_name='Cuenta corriente', unique=True, blank=False, null=False)
    tarifa = models.PositiveIntegerField(verbose_name='Tarifa', blank=False, null=False)
    local = models.CharField(verbose_name='Local', max_length=150, blank=True, null=True)
    nombreComercial = models.CharField(verbose_name='Nombre Comercial', max_length=150, blank=True, null=True)
    direccionComercial = models.CharField(verbose_name='Direccion Comercial', max_length=150, blank=True, null=True)
    provinciaComercial = models.CharField(verbose_name='Provincia Comercial', max_length=150, blank=True, null=True)
    email = models.EmailField(verbose_name='Correo', max_length=150, blank=True, null=True)
    telefono = models.PositiveIntegerField(verbose_name='Telefono', unique=True, blank=True, null=True)
    ejecucionObrasComercial = models.CharField(verbose_name='Tipo de ejecucion de obra comercial',
                                               choices=CHOICE_TIPO_OBRA_COMERCIAL, max_length=50, blank=True, null=True)
    representacionObrasEscenicas = models.BooleanField(default=False)
    comunicacionObrasAudioVisuales = models.BooleanField(default=False)

    class Meta:
        db_table = 'ContratoLicenciaPersonaNatural'
        verbose_name = 'ContratosLicenciaPersonaNatural'
        verbose_name_plural = 'ContratosLicenciaPersonaNatural'

    def __str__(self):
        return f'Contrato licencia a persona natural numero {self.numeroLicencia} perteneciente a: {self.fk_utilizador.nombre}.'


class ContratoLicenciaPersonaJuridica(ContratoLicenciaBase):
    fk_modalidad = models.ForeignKey(Modalidad, verbose_name='Actividad Comercial', blank=True, null=True,
                                     on_delete=models.CASCADE)
    resolucionUtilizador = models.CharField(verbose_name='Resolucion Utilizador', max_length=200, blank=True, null=True)
    fechaResolucionUtilizador = models.DateField(verbose_name='Fecha resolucion Utilizador', blank=True, null=True)
    emisionResolucionUtilizador = models.CharField(verbose_name='Resolucion utilizador (emitida/creda por)',
                                                   max_length=150, blank=True, null=True)
    resolucionFirmante = models.CharField(verbose_name='Resolucion del firmante', max_length=200, blank=True, null=True)
    fechaResolucionFirmante = models.DateField(verbose_name='Fecha resolucion firmante', blank=True, null=True)
    fk_municipioComercial = models.ForeignKey(Municipio, verbose_name='Municipio Comercial', related_name="municipioComercial", blank=True, null=True, on_delete=models.CASCADE)
    codigoOnei = models.CharField(verbose_name='Codigo Onei', max_length=50, unique=True, blank=True, null=True)
    tipo = models.CharField(verbose_name='Tipo', max_length=150, choices=CHOICE_TIPO_PERSONA_JURIDICA, blank=True, null=True)
    tarifa = models.PositiveIntegerField(verbose_name='Tarifa', blank=True, null=True)
    cuentaCorriente = models.BigIntegerField(verbose_name='Cuenta corriente', unique=True, blank=False, null=False)
    nombreFirmanteContrato = models.CharField(verbose_name='Nombre de quien firma el contrato', max_length=150, blank=False, null=False)
    cargoFirmanteContrato = models.CharField(verbose_name='Cargo de quien firma el contrato', max_length=150, blank=False, null=False)
    emitido = models.CharField(verbose_name='Emitido por', max_length=250, blank=True, null=True)
    nombreComercial = models.CharField(verbose_name='Nombre Comercial', max_length=150, blank=True, null=True)
    direccionComercial = models.CharField(verbose_name='Direccion Comercial', max_length=150, blank=True, null=True)
    provinciaComercial = models.CharField(verbose_name='Provincia Comercial', max_length=150, blank=True, null=True)
    email = models.EmailField(verbose_name='Correo', max_length=150, blank=True, null=True)
    telefono = models.PositiveIntegerField(verbose_name='Telefono', unique=True, blank=True, null=True)
    ejecucionObrasComercial = models.CharField(verbose_name='Tipo de ejecucion de obra comercial', choices=CHOICE_TIPO_OBRA_COMERCIAL, max_length=50, blank=True, null=True)
    representacionObrasEscenicas = models.BooleanField(default=False)
    comunicacionObrasAudioVisuales = models.BooleanField(default=False)

    class Meta:
        db_table = 'ContratoLicenciaPersonaJuridica'
        verbose_name = 'ContratosLicenciaPersonaJuridica'
        verbose_name_plural = 'ContratosLicenciaPersonaJuridica'

    def __str__(self):
        return f'Contrato licencia a persona juridica numero {self.numeroLicencia} perteneciente a: {self.fk_utilizador.nombre}.'

class Anexo72Gaviota(Anexo72Base):
    categoria = models.CharField(verbose_name='Categoria', max_length=150, blank=False, null=False)
    numeroHabitacion = models.PositiveIntegerField(verbose_name='Numero Habitacion', blank=False, null=False)
    periodo = models.CharField(verbose_name='Periodo', max_length=150, blank=False, null=False)
    tarifaTemporadaAlta = models.PositiveIntegerField(verbose_name='Temporada alta', blank=False, null=False)
    tarifaTemporadaBaja = models.PositiveIntegerField(verbose_name='Temporada baja', blank=False, null=False)
    tarifaOcupacionInferior = models.PositiveIntegerField(verbose_name='Ocupacion por debajo del 30%', blank=False, null=False)
    importeTemporadaAlta = models.PositiveIntegerField(verbose_name='Importe', blank=True, null=True)
    importeTemporadaBaja = models.PositiveIntegerField(verbose_name='Importe', blank=True, null=True)
    importeTemporadaOcupacionInferior = models.PositiveIntegerField(verbose_name='Importe', blank=True, null=True)

    class Meta:
        db_table = 'Anexo72Gaviota'
        verbose_name = 'Anexos72Gaviota'
        verbose_name_plural = 'Anexos72Gaviota'

    def __str__(self):
        return f'Anexo 72 Gaviota vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Anexo72Cimex(Anexo72Base):
    locacionModalidad = models.CharField(verbose_name='Locacion', max_length=150, blank=False, null=False)
    cantidadPlazas = models.PositiveIntegerField(verbose_name='Cantidad de plazas', blank=False, null=False)
    tarifa = models.CharField(verbose_name='Tarifa', max_length=150, blank=False, null=False)
    importe = models.PositiveIntegerField(verbose_name='Importe', blank=True, null=True)

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
    importe = models.PositiveIntegerField(verbose_name='Importe', blank=True, null=True)

    class Meta:
        db_table = 'Anexo72TRD'
        verbose_name = 'Anexos72TRD'
        verbose_name_plural = 'Anexos72TRD'

    def __str__(self):
        return f'Anexo 72 TRD vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Anexo71Musica(Anexo71Base):
    tipoMusica = models.CharField(verbose_name='Tipo musica', choices=CHOICE_TIPO_OBRA_COMERCIAL, max_length=150, blank=False, null=False)
    modalidad = models.CharField(verbose_name='Modalidad', max_length=150, blank=False, null=False)
    periocidadEntrega = models.CharField(verbose_name='Periocidad de entrega', choices=CHOICE_PERIOCIDAD_ENTREGA, max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Anexo71Musica'
        verbose_name = 'Anexos71Musica'
        verbose_name_plural = 'Anexos71Musica'

    def __str__(self):
        return f'Anexo 71 musica vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Anexo71AudioVisual(Anexo71Base):
    categoriaAudiovisual = models.CharField(verbose_name='Categoria', choices=CHOICE_CATEGORIA_AUDIOVISUAL, max_length=150, blank=False, null=False)
    periocidadEntrega = models.CharField(verbose_name='Periocidad de entrega', choices=CHOICE_PERIOCIDAD_ENTREGA, max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Anexo71AudioVisual'
        verbose_name = 'Anexos71AudioVisual'
        verbose_name_plural = 'Anexos71AudioVisual'

    def __str__(self):
        return f'Anexo 71 audiovisual  vinculado al contrato {self.fk_contratoLicenciaEstatal.numeroLicencia}.'

class Proforma(models.Model):
    resolucion = models.PositiveIntegerField(verbose_name='Resolucion', blank=True, null=True)
    nombre = models.CharField(verbose_name='Nombre', max_length=250, blank=False, null=False)
    titulo = models.CharField(verbose_name='Titulo', max_length=255, blank=True, null=True)
    encabezado = models.TextField(verbose_name='Encabezado de la proforma', blank=True, null=True)
    descripcion = models.TextField(verbose_name='Cuerpo de la proforma', blank=False, null=False)
    descripcion2daParte = models.TextField(verbose_name='Cuerpo de la proforma seguda parte', blank=True, null=True)
    descripcion3raParte = models.TextField(verbose_name='Cuerpo de la proforma tercera parte', blank=True, null=True)
    tipo = models.PositiveIntegerField(verbose_name='Tipo Proforma', choices=CHOICE_TIPO_PROFORMA, blank=True, null=True)

    class Meta:
        db_table = 'Proforma'
        verbose_name = 'Proforma'
        verbose_name_plural = 'Proformas'

    def __str__(self):
        return f'Proforma: {self.nombre}.'

class ClasificadorProforma(models.Model):
    fk_proforma = models.ForeignKey('Proforma', verbose_name='Proforma', blank=True, null=True, on_delete=models.CASCADE)
    fk_sector = models.ForeignKey(Sector, verbose_name='Sector al que pertenece', blank=True, null=True, on_delete=models.CASCADE)
    tipo = models.CharField(verbose_name='Tipo', max_length=50, choices=CHOICE_UTILIZADOR, blank=False, null=False)
    tipoDerecho = models.CharField(verbose_name='Tipo de Derecho', max_length=50, choices=CHOICE_DERECHOS, blank=True, null=True)

    class Meta:
        db_table = 'ClasificadorProforma'
        verbose_name = 'ClasificadorProforma'
        verbose_name_plural = 'ClasificadorProformas'

    def __str__(self):
        return f'Clasificador: {self.fk_proforma.nombre}--{self.tipo}.'


class Suplemento(models.Model):
    fk_usuario = models.ForeignKey(Usuario, verbose_name='Creado por', blank=True, null=True, on_delete=models.CASCADE)
    fk_contratoLicenciaEstatal = models.ForeignKey(ContratoLicenciaEstatal, verbose_name='Contrato Estatal', blank=True, null=True, on_delete=models.CASCADE)
    fk_contratoLicenciaPersonaJuridica = models.ForeignKey(ContratoLicenciaPersonaJuridica, verbose_name='Contrato Persona Juridica', blank=True, null=True, on_delete=models.CASCADE)
    fk_contratoLicenciaPersonaNatural = models.ForeignKey(ContratoLicenciaPersonaNatural, verbose_name='Contrato Persona Natural', blank=True, null=True, on_delete=models.CASCADE)
    fechaCreacion = models.DateField(verbose_name='Fecha en que se crea el suplemento', auto_now=True)
    titulo = models.CharField(verbose_name='Titulo', max_length=255, blank=True, null=True)
    codigo = models.IntegerField(verbose_name='Codigo', blank=True, null=True)
    direccion = models.CharField(verbose_name='Direccion', max_length=255, blank=True, null=True)
    cuentaBancaria = models.BigIntegerField(verbose_name='Cuenta Bancaria', unique=True, blank=True, null=True)
    sucursal = models.CharField(verbose_name='Sucursal', max_length=150, blank=True, null=True)
    nombreFirmanteContrato = models.CharField(verbose_name='Nombre de quien firma el contrato', max_length=150,
                                              blank=True, null=True)
    cargoFirmanteContrato = models.CharField(verbose_name='Cargo de quien firma el contrato', max_length=150,
                                             blank=True, null=True)
    resolucionFirmante = models.CharField(verbose_name='Resolucion del firmante', max_length=200, blank=True, null=True)
    fechaResolucionFirmante = models.DateField(verbose_name='Fecha resolucion firmante', blank=True, null=True)
    descripcion = models.TextField(verbose_name='Cuerpo del suplemento', blank=False, null=False)

    class Meta:
        db_table = 'Suplemento'
        verbose_name = 'Suplemento'
        verbose_name_plural = 'Suplementos'

    def __str__(self):
        return f'{self.titulo}.'


