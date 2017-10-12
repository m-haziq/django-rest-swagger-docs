from django.conf.urls import url, include
from .swagger_schema import SwaggerSchemaView

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^cbv/', include('demo.cbv_demo.urls')),
    url(r'^fbv/', include('demo.fbv_demo.urls')),
    url(r'^swagger/', SwaggerSchemaView.as_view()),
]
