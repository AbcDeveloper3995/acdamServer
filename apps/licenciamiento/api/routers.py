from rest_framework.routers import DefaultRouter

from apps.licenciamiento.api.views import *

router = DefaultRouter()
router.register(r'sector', sectorViewSet, basename='sectorViewSet'),
router.register(r'modalidad', modalidadViewSet, basename='modalidadViewSet'),
router.register(r'municipio', municipioViewSet, basename='municipioViewSet')
router.register(r'utilizador', utilizadorViewSet, basename='utilizadorViewSet')
router.register(r'representante', representanteViewSet, basename='representanteViewSet')
router.register(r'proforma', proformaViewSet, basename='proformaViewSet')
router.register(r'contratoLicenciaEstatal', contratoLicenciaEstatalViewSet, basename='contratoLicenciaEstatalViewSet')
router.register(r'contratoLicenciaPersonaJuridica', contratoLicenciaPersonaJuridicaViewSet, basename='contratoLicenciaPersonaJuridicaViewSet')
router.register(r'contratoLicenciaPersonaNatural', contratoLicenciaPersonaNaturalViewSet, basename='contratoLicenciaPersonaNaturalViewSet')

urlpatterns = router.urls