from django.conf.urls import url
from django.contrib import admin

from cbv_demo.views import UserViewSet

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^cbv_demo/user', UserViewSet.as_view()),
]
