from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from apps.usuario.api.serializers import *
from apps.utils import getElementosPaginados


class Login(TokenObtainPairView):
    serializer_class = customTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        usuario = authenticate(username=username, password=password)
        if usuario:
            login_serializers = self.serializer_class(data=request.data)
            if login_serializers.is_valid():
                usuario_serializer = customUsuarioSerializer(usuario)
                return Response({
                    'token': login_serializers.validated_data.get('access'),
                    'refresh-token': login_serializers.validated_data.get('refresh'),
                    'usuario': usuario_serializer.data,
                    'message': 'Inicio de sesion exitoso.'
                }, status=status.HTTP_200_OK)
            return Response({'error': login_serializers.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Contrasena o nombre de usuario incorrectos'}, status=status.HTTP_400_BAD_REQUEST)


class Logout(GenericAPIView):

    def post(self, request, *args, **kwargs):
        usuario = Usuario.objects.filter(id=request.data.get('usuario', 0))
        if usuario.exists():
            RefreshToken.for_user(usuario.first())
            return Response({'message':'Se ha cerrado su sesion.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'error': 'Usuario no encontrado.'}, status=status.HTTP_400_BAD_REQUEST)

#API DE CARGO
class cargoViewSet(viewsets.ModelViewSet):
    serializer_class = cargoSerializer
    list_serializer_class = cargoListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.list_serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()

    def get_object(self, pk):
        return get_object_or_404(self.list_serializer_class.Meta.model, pk=pk)

    def list(self, request, *args, **kwargs):
        """Documentacion para listar cargos

           Aca encontrara lo necesario a tener en cuenta para la funcionalidad de listar cargos"""
        serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Cargo creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        cargo = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(cargo)
        return Response({'message': 'Detalles del cargo', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            serializer = self.serializer_class(self.get_queryset(pk), data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'message': 'Cargo modificado correctamente', 'data': serializer.data},
                                status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Cargo no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        cargo = self.get_queryset(pk)
        if cargo:
            cargo.delete()
            return Response({'message': 'Cargo eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Cargo no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Cargo, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

class usuarioViewSet(viewsets.GenericViewSet):
    model = Usuario
    serializer_class = usuarioSerializer
    list_serializer_class = usuarioListarSerializer
    queryset = None

    def get_object(self, pk):
        return get_object_or_404(self.model, pk=pk)

    def get_queryset(self):
        if self.queryset is None:
            self.queryset = self.model.objects.filter(is_active=True)
        return self.queryset

    def list(self, request):
        usuarios = self.get_queryset()
        serializer = self.list_serializer_class(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        usuario = self.get_object(self.kwargs['pk'])
        serializer = self.serializer_class(usuario)
        return Response({'message': 'Detalles del usuario', 'data': serializer.data}, status=status.HTTP_200_OK)

    def update(self, request, pk=None):
         usuario = self.get_object(pk)
         serializer = usuarioSerializer(usuario, data=request.data)
         if serializer.is_valid():
             usuario.groups.clear()
             for i in request.data['groups']:
                 usuario.groups.add(i)
             if usuario.password != request.data['password']:
                 usuario.set_password(request.data['password'])
                 usuario.save()
             serializer.save()
             return Response({'message': 'Usuario actualizado correctamente'}, status=status.HTTP_200_OK)
         return Response({'message': 'Ha ocurrido un error en la actualizacion', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        usuario = self.model.objects.filter(id=pk).update(is_active=False)
        if usuario == 1:
            return Response({'message': 'Usuario eliminado correctamente '}, status=status.HTTP_200_OK)
        return Response({'message': 'Usuario no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'], url_path='paginado')
    def paginado(self, request, *args, **kwargs):
        data = getElementosPaginados(self.kwargs['pk'], Usuario, self.list_serializer_class)
        return Response(data, status=status.HTTP_200_OK)

class grupoViewSet(viewsets.ModelViewSet):
    serializer_class = grupoSerializer
    list_serializer_class = grupoListarSerializer

    def get_queryset(self, pk=None):
        if pk is None:
            return self.serializer_class.Meta.model.objects.all()
        return self.serializer_class.Meta.model.objects.filter(id=pk).first()


    def list(self, request, *args, **kwargs):
        grupo_serializer = self.list_serializer_class(self.get_queryset(), many=True)
        return Response(grupo_serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        grupo_serializer = self.serializer_class(data=request.data)
        if grupo_serializer.is_valid():
            grupo_serializer.save()
            return Response({'message': 'Grupo creado correctamente'}, status=status.HTTP_201_CREATED)
        return Response(grupo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        if self.get_queryset(pk):
            grupo_serializer = self.serializer_class(instance=self.get_queryset(pk), data=request.data)
            if grupo_serializer.is_valid():
                grupo_serializer.save()
                return Response({'message': 'Grupo modificado correctamente', 'data': grupo_serializer.data},
                                status=status.HTTP_200_OK)
            return Response(grupo_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Grupo no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        grupo = self.get_queryset(pk)
        if grupo:
            grupo.delete()
            return Response({'message': 'El Grupo se ha eliminado correctamente.'}, status=status.HTTP_200_OK)
        return Response({'message': 'Grupo no encontrado'}, status=status.HTTP_400_BAD_REQUEST)

