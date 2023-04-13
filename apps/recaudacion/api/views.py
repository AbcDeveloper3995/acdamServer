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

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Credito, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)
