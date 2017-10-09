from django.conf.urls import url

from .views import Contact

urlpatterns = [
    url(r'^contact', Contact.as_view(), name='contact'),
]