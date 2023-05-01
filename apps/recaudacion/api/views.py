import datetime
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.db.models import Q
from django.shortcuts import get_object_or_404


from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from acdamBackend import settings
from apps.licenciamiento.models import Representante
from apps.recaudacion.api.serializers import *
from apps.utils import getElementosPaginados


#API DE CONCEPTO
class conceptoViewSet(viewsets.ModelViewSet):
    serializer_class = conceptoSerializer
    list_serializer_class = conceptoListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Concepto creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        concepto = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(concepto)
        return Response({'message': 'Detalles del concepto', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Concepto modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Concepto no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        concepto = self.get_queryset(pk)
        if concepto:
            concepto.delete()
            return Response({'message': 'Concepto eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Concepto no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Concepto, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

#API DE SUCURSAL
class sucursalViewSet(viewsets.ModelViewSet):
    serializer_class = sucursalSerializer
    list_serializer_class = sucursalListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Sucursal creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        sucursal = self.get_object(self.kwargs['pk'])
        serializer = self.list_serializer_class(sucursal)
        return Response({'message': 'Detalles de la sucursal', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Sucursal modificada correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Sucursal no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sucursal = self.get_queryset(pk)
        if sucursal:
            sucursal.delete()
            return Response({'message': 'Sucursal eliminada correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Sucursal no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Sucursal, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

#API DE RECAUDACION
class recaudacionViewSet(viewsets.ModelViewSet):
    serializer_class = recaudacionSerializer
    list_serializer_class = recaudacionListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Recaudacion creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        recaudacion = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(recaudacion)
        return Response({'message': 'Detalles de la recaudacion', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Recaudacion modificada correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Recaudacion no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        recaudacion = self.get_queryset(pk)
        if recaudacion:
            recaudacion.delete()
            return Response({'message': 'Recaudacion eliminada correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Recaudacion no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Recaudacion, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='getRecaudacionUltimas4')
    def getRecaudacionUltimas4(self, request, *args, **kwargs):
        final = Recaudacion.objects.all().count()
        query = Recaudacion.objects.all()[final-4:final]
        serializer = self.list_serializer_class(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE CREDITO
class creditoViewSet(viewsets.ModelViewSet):
    serializer_class = creditoSerializer
    list_serializer_class = creditoListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if str(request.data['provincia']).__len__() == 2 or str(request.data['provincia']).__len__() == 3:
            request.data['provincia'] = formatoLargoProvincia(request.data['provincia'])
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Credito creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        credito = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(credito)
        return Response({'message': 'Detalles del credito', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Credito modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Credito no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        credito = self.get_queryset(pk)
        if credito:
            credito.delete()
            return Response({'message': 'Credito eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Credito no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def getImportesPorProvincia(self, provincias, arrayImportes, obj):
        arrayImportes.append(float(obj.importe))
        provincias[obj.provincia] = arrayImportes
        return provincias

    def getTotalImportesPorProvincia(self, provincias, array):
        for i in provincias.values():
            suma = 0
            for j in i:
                suma += j
            array.append(suma)
        return array

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        parametros = self.kwargs['pk'].split('-')
        numeroPagina = parametros[0]
        idRecaudacion = parametros[1]
        data = getElementosPaginados(numeroPagina, Credito, self.list_serializer_class, idRecaudacion)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='resumenProvincias')
    def resumenProvincias(self, request, *args, **kwargs):
        data, provincias, creditos , aux, totalesCheques, totalesTransferencias = {}, {}, [], [], [], []
        #DECLARACION DE LAS LISTAS PARA TODOS LOS IMPORTES CHEQUES DE CADA PROVINCIA
        importePRcheque, importeARTcheque, importeHABcheque, importeMAYcheque, importeMTZcheque, importeVCLcheque, importeCFGcheque = [], [], [], [], [], [], []
        importeSSPcheque, importeCAVcheque, importeTUNcheque, importeHOLcheque, importeGRMcheque, importeSTGcheque, importeGTMcheque  = [], [], [], [], [], [], []
        importeISJcheque, importeCMGcheque = [], []
        # DECLARACION DE LAS LISTAS PARA TODOS LOS IMPORTES TRANSFERENCIAS DE CADA PROVINCIA
        importePRtransferencia, importeARTtransferencia, importeHABtransferencia, importeMTZtransferencia, importeVCLtransferencia, importeCFGtransferencia = [], [], [], [], [], []
        importeSSPtransferencia, importeCAVtransferencia, importeTUNtransferencia, importeHOLtransferencia, importeGRMtransferencia, importeSTGtransferencia = [], [], [], [], [], []
        importeGTMtransferencia, importeISJtransferencia, importeCMGtransferencia, importeMAYtransferencia = [], [], [], []
        mes = self.kwargs['pk']
        queryCheque = Credito.objects.filter(Q(transferencia='') | Q(transferencia=None), fk_recaudacion__fechaCreacion__month=mes)
        queryTransferencia = Credito.objects.filter(Q(cheque='') | Q(cheque=None), fk_recaudacion__fechaCreacion__month=mes)

        #PROCESO DE OBTENCION DE LOS IMPORTES CHEQUES POR PROVINCIAS
        for i in queryCheque:
            if i.provincia == 'Pinar del Rio':
                data['cheque'] = self.getImportesPorProvincia(provincias, importePRcheque, i)
            elif i.provincia == 'Artemisa':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeARTcheque, i)
            elif i.provincia == 'La Habana':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeHABcheque, i)
            elif i.provincia == 'Mayabeque':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeMAYcheque, i)
            elif i.provincia == 'Matanzas':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeMTZcheque, i)
            elif i.provincia == 'Villa Clara':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeVCLcheque, i)
            elif i.provincia == 'Cienfuegos':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeCFGcheque, i)
            elif i.provincia == 'Santi Spiritu':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeSSPcheque, i)
            elif i.provincia == 'Ciego de Avila':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeCAVcheque, i)
            elif i.provincia == 'Camaguey':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeCMGcheque, i)
            elif i.provincia == 'Las Tunas':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeTUNcheque, i)
            elif i.provincia == 'Holguin':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeHOLcheque, i)
            elif i.provincia == 'Granma':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeGRMcheque, i)
            elif i.provincia == 'Santiago de Cuba':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeSTGcheque, i)
            elif i.provincia == 'Guantanamo':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeGTMcheque, i)
            else:
                data['cheque'] = self.getImportesPorProvincia(provincias, importeISJcheque, i)
        data['totalesCheques'] = self.getTotalImportesPorProvincia(provincias, totalesCheques)
        aux.append(data)

        # PROCESO DE OBTENCION DE LOS IMPORTES TRANSFERENCIAS POR PROVINCIAS
        data, provincias = {}, {}
        for i in queryTransferencia:
            if i.provincia == 'Pinar del Rio':
                data['transferencia'] = self.getImportesPorProvincia(provincias, importePRtransferencia, i)
            elif i.provincia == 'Artemisa':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeARTtransferencia, i)
            elif i.provincia == 'La Habana':
                data['transferencia'] = self.getImportesPorProvincia(provincias, importeHABtransferencia, i)
            elif i.provincia == 'Mayabeque':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeMAYtransferencia, i)
            elif i.provincia == 'Matanzas':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeMTZtransferencia, i)
            elif i.provincia == 'Villa Clara':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeVCLtransferencia, i)
            elif i.provincia == 'Cienfuegos':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeCFGtransferencia, i)
            elif i.provincia == 'Santi Spiritu':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeSSPtransferencia, i)
            elif i.provincia == 'Ciego de Avila':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeCAVtransferencia, i)
            elif i.provincia == 'Camaguey':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeCMGtransferencia, i)
            elif i.provincia == 'Las Tunas':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeTUNtransferencia, i)
            elif i.provincia == 'Holguin':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeHOLtransferencia, i)
            elif i.provincia == 'Granma':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeGRMtransferencia, i)
            elif i.provincia == 'Santiago de Cuba':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeSTGtransferencia, i)
            elif i.provincia == 'Guantanamo':
                data['cheque'] = self.getImportesPorProvincia(provincias, importeGTMtransferencia, i)
            else:
                data['cheque'] = self.getImportesPorProvincia(provincias, importeISJtransferencia, i)
        data['totalesTransferencias'] = self.getTotalImportesPorProvincia(provincias, totalesTransferencias)
        aux.append(data)

        # PROCESO DE OBTENCION DEL TOTAL GENERAL DE LOS IMPORTES CUEQUES + TRANSFERENCIAS POR CADA PROVINCIA
        totalesGenerales = []
        for i in range(len(totalesCheques)):
            totalesGenerales.append(totalesCheques[i])
        for i in range(len(totalesTransferencias)):
            totalesGenerales[i] = totalesGenerales[i] + totalesTransferencias[i]
        data['totalesGenerales'] = totalesGenerales

        aux.append(data)
        return Response({'creditos':aux}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='acumuladoReal')
    def getAcumuladoReal(self, request, *args, **kwargs):
        data = {}
        parametros = self.kwargs['pk'].split(',')
        tipoFrontera, fecha, cont = parametros[0], parametros[1], 0
        if tipoFrontera == '1':
            query = Credito.objects.filter(Q(tipoEstatal=1) | Q(tipoEstatal=3), fk_recaudacion__fechaCreacion__lte=fecha).values('importe')
        elif tipoFrontera == '2':
            query = Credito.objects.filter(Q(tipoEstatal=2) | Q(tipoEstatal=4), fk_recaudacion__fechaCreacion__lte=fecha).values('importe')
        else:
            query = Credito.objects.filter(tipoEstatal=5, fk_recaudacion__fechaCreacion__lte=fecha).values('importe')
        for i in query:
            cont += i['importe']
        data['real'] = cont
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='enviarEmail')
    def sendEmail(self, request, *args, **kwargs):
        representantes = []
        parametros = self.kwargs['pk'].split(',')
        fecha, provincia = parametros[0], parametros[1]
        date = datetime.datetime.now().date()
        date = date - datetime.timedelta(days=1)
        cuerpoCorreo, index = 'Buenos dias \n\n', ''

        if fecha == '':
            cuerpoCorreo += f'Ingresos dia {date} \n'
            query = Credito.objects.filter(Q(cheque='') | Q(cheque=None), fk_recaudacion__fechaEstadoCuenta=date, provincia=formatoLargoProvincia(provincia))
            objs = Representante.objects.filter(provincia=provincia).values('email')
            for j in objs:
                representantes.append(j['email'])
            for i in query:
                cuerpoCorreo += f'{i.transferencia}, {i.fk_utilizador.nombre}, ${i.importe}, F-{i.factura}\n' if i.factura != None else f'{i.transferencia}, {i.fk_utilizador.nombre}, ${i.importe}\n'

        else:
            query = Credito.objects.filter(Q(cheque='') | Q(cheque=None), fk_recaudacion__fechaEstadoCuenta__range=(fecha,date), provincia=formatoLargoProvincia(provincia))
            objs = Representante.objects.filter(provincia=provincia).values('email')
            for j in objs:
                representantes.append(j['email'])
            for i in query:
                if i.fk_recaudacion.fechaEstadoCuenta != index:
                    cuerpoCorreo += f'\nIngresos dia {i.fk_recaudacion.fechaEstadoCuenta} \n {i.transferencia}, {i.fk_utilizador.nombre}, ${i.importe}, F-{i.factura}\n' if i.factura != None else f'\nIngresos dia {i.fk_recaudacion.fechaEstadoCuenta} \n {i.transferencia}, {i.fk_utilizador.nombre}, ${i.importe}\n'
                else:
                    cuerpoCorreo += f'{i.transferencia}, {i.fk_utilizador.nombre}, ${i.importe}, F-{i.factura}\n' if i.factura != None else f'{i.transferencia}, {i.fk_utilizador.nombre}, ${i.importe}\n'
                index = i.fk_recaudacion.fechaEstadoCuenta
        cuerpoCorreo += '\n\nSaludos.'
        data = {}
        try:
            emailServidor = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            emailServidor.starttls()
            emailServidor.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

            email = representantes
            sms = MIMEMultipart()
            sms['From'] = settings.EMAIL_HOST_USER
            sms['To'] = ','.join(email)
            sms['Subject'] = 'Ingresos Creditos'

            content = cuerpoCorreo
            sms.attach(MIMEText(content))
            emailServidor.sendmail(settings.EMAIL_HOST_USER, email, sms.as_string())
            data['sms'] = f'Se le ha enviado un correo a los representantes de la provincia {formatoLargoProvincia(provincia)} correctamente.'
        except Exception as e:
            print(str(e))
            data['error'] = 'Ha ocurrido un error. Contacte con el administrador.'
        return Response(data, status=status.HTTP_200_OK)

#API DE RESUMEN  RECAUDACION DIARIA
class resumenRecaudacionDiariaViewSet(viewsets.ModelViewSet):
    serializer_class = resumenRecaudacionSerializer
    list_serializer_class = resumenRecaudacionListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'El total de los ingresos de hoy se han registrado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        credito = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(credito)
        return Response({'message': 'Detalles del credito', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Credito modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Credito no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        credito = self.get_queryset(pk)
        if credito:
            credito.delete()
            return Response({'message': 'Credito eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Credito no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

#API DE RECAUDACION MENSUAL
class recaudacionMensualViewSet(viewsets.ModelViewSet):
    serializer_class = recaudacionMensualSerializer
    list_serializer_class = recaudacionMensualListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'El plan se ha establecido correctamente.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        plan = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(plan)
        return Response({'message': 'Detalles del plan', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Plan modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Plan no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        plan = self.get_queryset(pk)
        if plan:
            plan.delete()
            return Response({'message': 'Plan eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Plan no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getPlan')
    def getPlan(self, request, *args, **kwargs):
        query = RecaudacionMensual.objects.filter(codigo=self.kwargs['pk'])
        if not query.exists():
            return Response({'error': 'Aun no se ha creado un plan para este mes.'}, status=status.HTTP_400_BAD_REQUEST)
        plan = list(query).pop()
        serializer = recaudacionMensualListarSerializer(plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='actualizarReal')
    def actualizarReal(self, request, *args, **kwargs):
        real = json.loads(self.kwargs['pk'])
        codigo = real.get('codigo')
        realFronteraEstatal = float(real.get('realFronteraEstatal').replace(",","."))
        realFronteraTCP = float(real.get('realFronteraTCP').replace(",","."))
        realSociedad = float(real.get('realSociedad').replace(",","."))
        RecaudacionMensual.objects.filter(codigo=codigo).update(realFronteraEstatal=realFronteraEstatal,realFronteraTCP=realFronteraTCP,realSociedad=realSociedad)
        return Response({"message":'La recaudacion real se ha actualizado correctamenete.'}, status=status.HTTP_200_OK)

#API DE REPORTE COBRO UTILIZADOR
class reporteCobroUtilizadorViewSet(viewsets.ModelViewSet):
    serializer_class = reporteCobroUtilizadorSerializer
    list_serializer_class = reporteCobroUtilizadorListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        id = Credito.objects.filter(Q(cheque=request.data['fk_credito']) | Q(transferencia=request.data['fk_credito'])).values('id')
        request.data['fk_credito'] = id[0]['id']
        request.data['numeroReporteFecha'] = self.formatearNoReporteFecha(request.data['numeroReporte'],request.data['fecha'])
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'El reporte se ha establecido correctamente.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        plan = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(plan)
        return Response({'message': 'Detalles del reporte', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Reporte modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Reporte no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        plan = self.get_queryset(pk)
        if plan:
            plan.delete()
            return Response({'message': 'Reporte eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Reporte no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def formatearNoReporteFecha(self,numero,fecha):
        formato = fecha.split('-')
        dia = formato[2]
        mes = formato[1]
        ano = formato[0]
        formato = f'{numero}/{dia}/{mes}/{ano}'
        return formato

    @action(detail=True, methods=['get'], url_path='getReportes')
    def getReportes(self, request, *args, **kwargs):
        mes = datetime.datetime.now().date().month
        query = ReporteCobroUtilizador.objects.filter(fk_credito__fk_utilizador_id=self.kwargs['pk'], fechaCreacion__month=mes)
        serializer = reporteCobroUtilizadorListarSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    '''En esta accion se va a ir recorriendo por cada utilizador del un representante lo que va recaudando mes a mes por concepto
    y por modalidad, asi como su total real acumulado tanto por concepto y modalidad'''
    @action(detail=True, methods=['get'], url_path='getGestionGeneral')
    def getGestionGeneral(self, request, *args, **kwargs):
        data, listadoConceptos, listadoModalidades = {}, [], []
        # CONCEPTOS
        musicaViva = {'index': 'Musica Viva', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        musicaGrabada = {'index': 'Musica Grabada', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        derecho = {'index': 'G.Derecho', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        radio = {'index': 'Radio', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        tvMusica = {'index': 'TV-Musica', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        mora = {'index': 'Mora', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        tvAudiovisual = {'index': 'TV-Audiovisual', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        dramaticoCultutra = {'index': 'Dramatico Cultura', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0,'diciembre': 0}
        cineAudiovisual = {'index': 'Cine Audiovisual', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        cineDramatico = {'index': 'Cine Dramatico', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        # MODALIDADES
        modalidadBar = {'index': 'Modalidad Bar', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0,'diciembre': 0}
        modalidadCafeteria = {'index': 'Modalidad Cafeteria', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0,'noviembre': 0, 'diciembre': 0}
        modalidadRestaurante = {'index': 'Modalidad Restaurante', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0,'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0, 'noviembre': 0, 'diciembre': 0}
        modalidadCentroNocturno = {'index': 'Modalidad C/Nocturno', 'enero': 0, 'febrero': 0, 'marzo': 0, 'abril': 0, 'mayo': 0, 'junio': 0, 'julio': 0, 'agosto': 0, 'septiembre': 0, 'octubre': 0,'noviembre': 0, 'diciembre': 0}
        #TOTALES CONCEPTOS
        totalMusicaViva = totalMusciaGrabada = totalDerecho = totalRadio = totalTVmusica = totalMora = totalTVaudiovisual = totalDramatico = totalCineAudiovisual = totalCineDramatico = 0
        # TOTALES MODALIDADES
        totalBar = totalCafeteria = totalRestaurante = totalCentroNocturno = 0

        query = Representante.objects.filter(pk=self.kwargs['pk'])

        if not query.exists():
            return Response({'error': 'No ha seleccionado un representante.'}, status=status.HTTP_400_BAD_REQUEST)
        utilizadores = query[0].fk_utilizador.all()
        for i in utilizadores:
            objs = ReporteCobroUtilizador.objects.filter(fk_credito__fk_utilizador_id=i.pk)
            for j in objs:
                musicaViva, totalMusicaViva = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoMusicaViva, musicaViva, totalMusicaViva)
                musicaGrabada, totalMusciaGrabada = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoMusicaGrabada, musicaGrabada, totalMusciaGrabada)
                derecho, totalDerecho = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoDerecho, derecho, totalDerecho)
                radio, totalRadio = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoRadio, radio, totalRadio)
                tvMusica, totalTVmusica = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoTVmusica, tvMusica, totalTVmusica)
                mora, totalMora = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoMora, mora, totalMora)
                tvAudiovisual, totalTVaudiovisual = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoTVaudiovisual, tvAudiovisual, totalTVaudiovisual)
                dramaticoCultutra, totalDramatico = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoDramatico, dramaticoCultutra, totalDramatico)
                cineAudiovisual, totalCineAudiovisual = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoCineAudiovisual, cineAudiovisual, totalCineAudiovisual)
                cineDramatico, totalCineDramatico = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoCineDramatico, cineDramatico, totalCineDramatico)
                modalidadBar, totalBar = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoBar, modalidadBar, totalBar)
                modalidadCafeteria, totalCafeteria = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoCafeteria, modalidadCafeteria, totalCafeteria)
                modalidadRestaurante, totalRestaurante = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoRestaurante, modalidadRestaurante, totalRestaurante)
                modalidadCentroNocturno, totalCentroNocturno = self.getTotalPorMesyTotalGeneral(j.fechaCreacion, j.montoCNocturno, modalidadCentroNocturno, totalCentroNocturno)

        listadoConceptos.append(musicaViva)
        listadoConceptos.append(musicaGrabada)
        listadoConceptos.append(derecho)
        listadoConceptos.append(radio)
        listadoConceptos.append(tvMusica)
        listadoConceptos.append(mora)
        listadoConceptos.append(tvAudiovisual)
        listadoConceptos.append(dramaticoCultutra)
        listadoConceptos.append(cineAudiovisual)
        listadoConceptos.append(cineDramatico)
        data['conceptos'] = listadoConceptos
        listadoModalidades.append(modalidadBar)
        listadoModalidades.append(modalidadCafeteria)
        listadoModalidades.append(modalidadRestaurante)
        listadoModalidades.append(modalidadCentroNocturno)
        data['modalidades'] = listadoModalidades
        return Response(data, status=status.HTTP_200_OK)

    def getTotalPorMesyTotalGeneral(self, fecha, atributo, data, total):
        meses = {1: 'enero', 2: 'febrero', 3: 'febrero', 4: 'abril', 5: 'mayo', 6: 'junio', 7: 'julio', 8: 'agosto', 9: 'septiembre', 10: 'octubre', 11: 'noviembre', 12: 'diciembre'}
        for i in range(1, 13):
            if fecha.month == i:
                suma = 0
                suma += atributo
                mes = meses[i]
                aux = data[mes]
                data[mes] = aux + suma
        total += atributo
        data['totalReal'] = total
        return data, total