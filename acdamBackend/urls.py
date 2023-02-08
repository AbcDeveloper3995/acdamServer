from django.contrib import admin
from django.urls import path, re_path, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


#from apps.usuario.api.views import Login, Logout
from apps.usuario.api.views import Login, Logout

schema_view = get_schema_view(
   openapi.Info(
      title="ACDAM API",
      default_version='v1',
      description="Documentacion de todas las apis del proyecto ACDAM",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('usuario/', include('apps.usuario.api.routers')),
    # path('licenciamiento/', include('apps.licenciamiento.api.routers')),
]

urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)