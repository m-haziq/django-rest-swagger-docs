from django.conf.urls import url
from .views import save_medical, get_medical


urlpatterns = [
    url(r'^save_medical', save_medical, name='save_contact'),
    url(r'^get_medical', get_medical, name='get_contact'),
]