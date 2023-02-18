from rest_framework.routers import DefaultRouter

from apps.licenciamiento.api.views import *

router = DefaultRouter()
router.register(r'sector', sectorViewSet, basename='sectorViewSet'),
router.register(r'municipio', municipioViewSet, basename='municipioViewSet')
router.register(r'utilizador', utilizadorViewSet, basename='utilizadorViewSet')
router.register(r'representante', representanteViewSet, basename='representanteViewSet')

urlpatterns = router.urls