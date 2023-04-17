from rest_framework.routers import DefaultRouter

from apps.recaudacion.api.views import *

router = DefaultRouter()
router.register(r'concepto', conceptoViewSet, basename='conceptoViewSet'),
router.register(r'sucursal', sucursalViewSet, basename='sucursalViewSet'),
router.register(r'recaudacion', recaudacionViewSet, basename='recaudacionViewSet'),
router.register(r'credito', creditoViewSet, basename='creditoViewSet'),
router.register(r'resumenRecaudacion', resumenRecaudacionDiariaViewSet, basename='resumenRecaudacionDiariaViewSet'),
router.register(r'recaudacionMensual', recaudacionMensualViewSet, basename='recaudacionMensualViewSet'),

urlpatterns = router.urls