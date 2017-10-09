from django.conf.urls import url

from .views import save_contact, get_contact

urlpatterns = [
    url(r'^save_contact', save_contact, name='save_contact'),
    url(r'^get_contact', get_contact, name='get_contact'),
]