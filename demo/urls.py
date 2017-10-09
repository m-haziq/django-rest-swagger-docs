from django.conf.urls import url, include

urlpatterns = [
    url(r'^cbv/', include('demo.cbv_demo.urls')),
    url(r'^fbv/', include('demo.fbv_demo.urls')),
]
