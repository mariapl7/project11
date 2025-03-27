from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from rest_framework.documentation import include_docs_urls
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.contrib import admin

schema_view = get_schema_view(
   openapi.Info(
      title="API",
      default_version='v1',
      description="Описание API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('courses.urls')),
    path('docs/', schema_view.as_view(), name='swagger-docs'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('payments/', include('payments.urls')),  # Добавляем маршруты для платежей
]
