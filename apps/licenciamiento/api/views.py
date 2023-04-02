from datetime import timedelta

from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.licenciamiento.api.serializers import *
from apps.utils import getElementosPaginados, getFechaExpiracion


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

#API DE MODALIDAD
class modalidadViewSet(viewsets.ModelViewSet):
    serializer_class = modalidadSerializer
    list_serializer_class = modalidadListarSerializer

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
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Modalidad creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        sector = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(sector)
        return Response({'message': 'Detalles de la modalidad', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Modalidad modificada correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Modalidad no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        sector = self.get_queryset(pk)
        if sector:
            sector.delete()
            return Response({'message': 'Modalidad eliminada correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Modalidad no encontrada'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Modalidad, self.list_serializer_class)
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
        aux, profomorma = [], []
        utilizador = self.get_object(self.kwargs['pk'])
        serializer = self.list_serializer_class(utilizador)
        idSector = utilizador.fk_sector.id
        derecho = utilizador.tipoDerecho
        if utilizador.tipo == '1':
            proformas = ClasificadorProforma.objects.filter(fk_sector__id=idSector, tipoDerecho=derecho)
            for i in proformas:
                aux.append(i.fk_proforma)
        else:
            proformas = ClasificadorProforma.objects.filter(tipo='2')
            for i in proformas:
                aux.append(i.fk_proforma)
        serializerProforma = proformaSerializer(aux, many=True)
        return Response({'idSector': idSector, 'tipo': utilizador.tipo, 'data': serializer.data, 'proformas':serializerProforma.data}, status=status.HTTP_200_OK)

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

    @action(detail=False, methods=['get'], url_path='getUtilizadoresSinContrato')
    def getUtilizadoresSinContrato(self, request, *args, **kwargs):
        query = Utilizador.objects.filter(tieneContrato=False)
        serializer = utilizadorListarSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    @action(detail=True, methods=['get'], url_path='getMunicipios')
    def getMunicipios(self, request, *args, **kwargs):
        slug = self.kwargs['pk']
        if slug == 'PR':
            municipios = Municipio.objects.filter(codigo=1)
        elif slug == 'ART':
            municipios = Municipio.objects.filter(codigo=2)
        elif slug == 'HAB':
            municipios = Municipio.objects.filter(codigo=3)
        elif slug == 'MAY':
            municipios = Municipio.objects.filter(codigo=4)
        elif slug == 'MAT':
            municipios = Municipio.objects.filter(codigo=5)
        elif slug == 'VCL':
            municipios = Municipio.objects.filter(codigo=6)
        elif slug == 'CFG':
            municipios = Municipio.objects.filter(codigo=7)
        elif slug == 'SS':
            municipios = Municipio.objects.filter(codigo=8)
        elif slug == 'CAV':
            municipios = Municipio.objects.filter(codigo=9)
        elif slug == 'TUN':
            municipios = Municipio.objects.filter(codigo=10)
        elif slug == 'HOL':
            municipios = Municipio.objects.filter(codigo=11)
        elif slug == 'STG':
            municipios = Municipio.objects.filter(codigo=12)
        elif slug == 'GTM':
            municipios = Municipio.objects.filter(codigo=13)
        elif slug == 'IJV':
            municipios = Municipio.objects.filter(codigo=14)
        serializer = municipioSerializer(municipios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def limpiarYasignarCamposMTM(self, campo, lista):
        campo.clear()
        for i in lista:
            campo.add(i)


#API DE CONTRATO  LICENCIA ESTATAL
class contratoLicenciaEstatalViewSet(viewsets.ModelViewSet):
    serializer_class = contratoLicenciaEstatalSerializer
    list_serializer_class = contratoLicEstatalListarSerializer

    def get_queryset(self, pk=None):
        date = datetime.datetime.now().date()
        fechaExpiracion = date + timedelta(days=7)
        ContratoLicenciaEstatal.objects.filter(fechaVecimiento=fechaExpiracion).update(estadoVigencia=2)
        ContratoLicenciaEstatal.objects.filter(fechaVecimiento__lte=date).update(estadoVigencia=3)
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.data['tiempoVigencia'] == None:
            request.data['fechaVecimiento'] = getFechaExpiracion(int(request.data['tiempoVigencia']))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            Utilizador.objects.filter(pk=request.data['fk_utilizador']).update(tieneContrato=True)
            serializer.save()
            return Response({'message': 'Contrato creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        contrato = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(contrato)
        return Response({'message': 'Detalles del Contrato', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Contrato modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            contrato.delete()
            return Response({'message': 'Contrato eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getlastContrato')
    def getlastContrato(self, request, *args, **kwargs):
        date = datetime.datetime.now().date()
        query = ContratoLicenciaEstatal.objects.filter(fk_usuario__id=self.kwargs['pk'], fechaCreacionContrato=date)
        if not query.exists():
            return Response({'error': 'El contrato no ha sido creado.'}, status=status.HTTP_400_BAD_REQUEST)
        contrato = list(query).pop()
        serializer = contratoLicenciaEstatalSerializer(contrato)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE PROFORMA
class proformaViewSet(viewsets.ModelViewSet):
    serializer_class = proformaSerializer
    list_serializer_class = proformaListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Proforma creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        proforma = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(proforma)
        return Response({'message': 'Detalles del proforma', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        proforma = self.get_queryset(pk)
        if proforma:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Proforma modificada correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Proforma no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        proforma = self.get_queryset(pk)
        if proforma:
            proforma.delete()
            return Response({'message': 'Proforma eliminada correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Proforma no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Proforma, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'], url_path='getProformaRepresentante')
    def getProformaRepresentante(self, request, *args, **kwargs):
        proforma = get_object_or_404(self.list_serializer_class.Meta.model, tipo=5)
        return Response({'idProformaRepresentante': proforma.pk}, status=status.HTTP_200_OK)

#API DE CONTRATO  LICENCIA NO ESTATAL PERSONA JURIDICA
class contratoLicenciaPersonaJuridicaViewSet(viewsets.ModelViewSet):
    serializer_class = contratoLicenciaPersonaJuridicaSerializer
    list_serializer_class = contratoLicenciaPersonaJuridicaListarSerializer

    def get_queryset(self, pk=None):
        date = datetime.datetime.now().date()
        fechaExpiracion = date + timedelta(days=7)
        ContratoLicenciaPersonaJuridica.objects.filter(fechaVecimiento=fechaExpiracion).update(estadoVigencia=2)
        ContratoLicenciaPersonaJuridica.objects.filter(fechaVecimiento__lte=date).update(estadoVigencia=3)
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.data['tiempoVigencia'] == None:
            request.data['fechaVecimiento'] = getFechaExpiracion(int(request.data['tiempoVigencia']))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contrato creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        contrato = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(contrato)
        return Response({'message': 'Detalles del Contrato', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Contrato modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            contrato.delete()
            return Response({'message': 'Contrato eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getlastContrato')
    def getlastContrato(self, request, *args, **kwargs):
        date = datetime.datetime.now().date()
        query = ContratoLicenciaPersonaJuridica.objects.filter(fk_usuario__id=self.kwargs['pk'], fechaCreacionContrato=date)
        if not query.exists():
            return Response({'error': 'El contrato no ha sido creado.'}, status=status.HTTP_400_BAD_REQUEST)
        contrato = list(query).pop()
        serializer = contratoLicenciaPersonaJuridicaSerializer(contrato)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE CONTRATO  LICENCIA NO ESTATAL PERSONA NATURAL
class contratoLicenciaPersonaNaturalViewSet(viewsets.ModelViewSet):
    serializer_class = contratoLicenciaPersonaNaturalSerializer

    def get_queryset(self, pk=None):
        date = datetime.datetime.now().date()
        fechaExpiracion = date + timedelta(days=7)
        ContratoLicenciaPersonaNatural.objects.filter(fechaVecimiento=fechaExpiracion).update(estadoVigencia=2)
        ContratoLicenciaPersonaNatural.objects.filter(fechaVecimiento__lte=date).update(estadoVigencia=3)
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        if not request.data['tiempoVigencia'] == None:
            request.data['fechaVecimiento'] = getFechaExpiracion(int(request.data['tiempoVigencia']))
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contrato creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        contrato = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(contrato)
        return Response({'message': 'Detalles del Contrato', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Contrato modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            contrato.delete()
            return Response({'message': 'Contrato eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getlastContrato')
    def getlastContrato(self, request, *args, **kwargs):
        date = datetime.datetime.now().date()
        query = ContratoLicenciaPersonaNatural.objects.filter(fk_usuario__id=self.kwargs['pk'], fechaCreacionContrato=date)
        if not query.exists():
            return Response({'error': 'El contrato no ha sido creado.'}, status=status.HTTP_400_BAD_REQUEST)
        contrato = list(query).pop()
        serializer = contratoLicenciaPersonaNaturalSerializer(contrato)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE ANEXO71MUSICA
class anexo71MusicaViewSet(viewsets.ModelViewSet):
    serializer_class = anexo71MusicaSerializer
    list_serializer_class = anexo71MusicaListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
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
            return Response({'message': 'Anexo musica creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        anexo71Musica = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(anexo71Musica)
        return Response({'message': 'Detalles del anexo musica', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        anexo71Musica = self.get_queryset(pk)
        if anexo71Musica:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Anexo musica modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Anexo musica no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        anexo71Musica = self.get_queryset(pk)
        if anexo71Musica:
            anexo71Musica.delete()
            return Response({'message': 'Anexo musica eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Anexo musica no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getAnexosDeUnContrato')
    def getAnexosDeUnContrato(self, request, *args, **kwargs):
        anexos = Anexo71Musica.objects.filter(fk_contratoLicenciaEstatal__pk=self.kwargs['pk'])
        serializer = self.list_serializer_class(anexos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE ANEXO71AUDIOVISUAL
class anexo71AudiovisualViewSet(viewsets.ModelViewSet):
    serializer_class = anexo71AudiovisualSerializer
    list_serializer_class = anexo71AudiovisualListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
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
            return Response({'message': 'Anexo audiovisual creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        anexo71Audiovisual = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(anexo71Audiovisual)
        return Response({'message': 'Detalles del anexo audiovisual', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        anexo71Audiovisual = self.get_queryset(pk)
        if anexo71Audiovisual:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Anexo audiovisual modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Anexo audiovisual no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        anexo71Audiovisual = self.get_queryset(pk)
        if anexo71Audiovisual:
            anexo71Audiovisual.delete()
            return Response({'message': 'Anexo audiovisual eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Anexo audiovisual no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getAnexosDeUnContrato')
    def getAnexosDeUnContrato(self, request, *args, **kwargs):
        anexos = Anexo71AudioVisual.objects.filter(fk_contratoLicenciaEstatal__pk=self.kwargs['pk'])
        serializer = self.list_serializer_class(anexos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE ANEXO72CIMEX
class anexo72CimexViewSet(viewsets.ModelViewSet):
    serializer_class = anexo72CimexSerializer
    list_serializer_class = anexo72CimexListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
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
            return Response({'message': 'Anexo cimex creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        anexo72Cimex = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(anexo72Cimex)
        return Response({'message': 'Detalles del anexo cimex', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        anexo71Audiovisual = self.get_queryset(pk)
        if anexo71Audiovisual:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Anexo cimex modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Anexo cimex no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        anexo72Cimex = self.get_queryset(pk)
        if anexo72Cimex:
            anexo72Cimex.delete()
            return Response({'message': 'Anexo cimex eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Anexo cimex no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getAnexosDeUnContrato')
    def getAnexosDeUnContrato(self, request, *args, **kwargs):
        anexos = Anexo72Cimex.objects.filter(fk_contratoLicenciaEstatal__pk=self.kwargs['pk'])
        serializer = self.list_serializer_class(anexos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE ANEXO72GAVIOTA
class anexo72GaviotaViewSet(viewsets.ModelViewSet):
    serializer_class = anexo72GaviotaSerializer
    list_serializer_class = anexo72GaviotaListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
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
            return Response({'message': 'Anexo gaviota creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        anexo72Gaviota = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(anexo72Gaviota)
        return Response({'message': 'Detalles del anexo gaviota', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        anexo72Gaviota = self.get_queryset(pk)
        if anexo72Gaviota:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Anexo gaviota modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Anexo gaviota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        anexo72Gaviota = self.get_queryset(pk)
        if anexo72Gaviota:
            anexo72Gaviota.delete()
            return Response({'message': 'Anexo gaviota eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Anexo gaviota no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getAnexosDeUnContrato')
    def getAnexosDeUnContrato(self, request, *args, **kwargs):
        anexos = Anexo72Gaviota.objects.filter(fk_contratoLicenciaEstatal__pk=self.kwargs['pk'])
        serializer = self.list_serializer_class(anexos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

#API DE ANEXO72TRD
class anexo72TrdViewSet(viewsets.ModelViewSet):
    serializer_class = anexo72TrdSerializer
    list_serializer_class = anexo72TrdListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
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
            return Response({'message': 'Anexo TRD creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        anexo72Trd = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(anexo72Trd)
        return Response({'message': 'Detalles del anexo TRD', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        anexo72Trd = self.get_queryset(pk)
        if anexo72Trd:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Anexo TRD modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Anexo TRD no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        anexo72Trd = self.get_queryset(pk)
        if anexo72Trd:
            anexo72Trd.delete()
            return Response({'message': 'Anexo TRD eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Anexo TRD no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getAnexosDeUnContrato')
    def getAnexosDeUnContrato(self, request, *args, **kwargs):
        anexos = Anexo72TRD.objects.filter(fk_contratoLicenciaEstatal__pk=self.kwargs['pk'])
        serializer = self.list_serializer_class(anexos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#API DE CONTRATO  MANDATO
class contratoMandatoViewSet(viewsets.ModelViewSet):
    serializer_class = contratoMandatoSerializer
    list_serializer_class = contratoMandatoListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Contrato creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        contrato = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(contrato)
        return Response({'message': 'Detalles del Contrato', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Contrato modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        contrato = self.get_queryset(pk)
        if contrato:
            contrato.delete()
            return Response({'message': 'Contrato eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Contrato no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='getlastContrato')
    def getlastContrato(self, request, *args, **kwargs):
        contrato = list(ContratoMandatoRepresentante.objects.filter(fk_usuario__id=self.kwargs['pk'])).pop()
        serializer = contratoMandatoListarSerializer(contrato)
        return Response(serializer.data, status=status.HTTP_200_OK)


#API DE CLASIFICADOR PROFORMA
class clasificadorProformaViewSet(viewsets.ModelViewSet):
    serializer_class = clasificadorProformaSerializer
    list_serializer_class = clasificadorProformaListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        serializer = self.serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Configuracion creada correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        proforma = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(proforma)
        return Response({'message': 'Detalles del Configuracion', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        proforma = self.get_queryset(pk)
        if proforma:
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Configuracion modificada correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Configuracion no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        proforma = self.get_queryset(pk)
        if proforma:
            proforma.delete()
            return Response({'message': 'Configuracion eliminada correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Configuracion no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], ClasificadorProforma, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)
