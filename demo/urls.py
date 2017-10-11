from django.conf.urls import url, include
from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='Demo Swagger API')

urlpatterns = [
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^cbv/', include('demo.cbv_demo.urls')),
    url(r'^fbv/', include('demo.fbv_demo.urls')),
    url(r'^swagger/', schema_view),
]
