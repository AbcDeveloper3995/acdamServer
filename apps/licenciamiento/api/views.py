from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.licenciamiento.api.serializers import *
from apps.utils import getElementosPaginados

#API DE SECTOR
class sectorViewSet(viewsets.ModelViewSet):
    serializer_class = sectorSerializer
    list_serializer_class = sectorListarSerializer

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
            return Response({'message': 'Sector creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        sector = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(sector)
        return Response({'message': 'Detalles del sector', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Sector modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Sector no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sector = self.get_queryset(pk)
        if sector:
            sector.delete()
            return Response({'message': 'Sector eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Sector no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Sector, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

#API DE MUNICIPIO
class municipioViewSet(viewsets.ModelViewSet):
    serializer_class = municipioSerializer
    list_serializer_class = municipioListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all().values('id', 'nombre')
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Municipio creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Municipio modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Municipio no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        municipio = self.get_queryset(pk)
        if municipio:
            municipio.delete()
            return Response({'message': 'Municipio eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Municipio no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

#API DE UTILIZADOR
class utilizadorViewSet(viewsets.ModelViewSet):
    serializer_class = utilizadorSerializer
    list_serializer_class = utilizadorListarSerializer

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
            return Response({'message': 'Utilizador creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        utilizador = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(utilizador)
        return Response({'message': 'Detalles del utilizador', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Utilizador modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Utilizador no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        utilizador = self.get_queryset(pk)
        if utilizador:
            utilizador.delete()
            return Response({'message': 'Utilizador eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Utilizador no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Utilizador, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

#API DE REPRESENTANTE
class representanteViewSet(viewsets.ModelViewSet):
    serializer_class = representanteSerializer
    list_serializer_class = representanteListarSerializer

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
            return Response({'message': 'Representante creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        representante = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(representante)
        return Response({'message': 'Detalles del representante', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        representante = self.get_queryset(pk)
        if representante:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                self.limpiarYasignarCamposMTM(representante.fk_municipio, request.data['fk_municipio'])
                self.limpiarYasignarCamposMTM(representante.fk_utilizador, request.data['fk_utilizador'])
                self.limpiarYasignarCamposMTM(representante.fk_sector, request.data['fk_sector'])
                serializer.save()
                return Response({'message': 'Representante modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Representante no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        representante = self.get_queryset(pk)
        if representante:
            representante.delete()
            return Response({'message': 'Representante eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Representante no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Representante, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

    def limpiarYasignarCamposMTM(self, campo, lista):
        campo.clear()
        for i in lista:
            campo.add(i)

