import datetime
import json

from django.db.models import Q
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

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
        plan = list(RecaudacionMensual.objects.filter(codigo=self.kwargs['pk'])).pop()
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