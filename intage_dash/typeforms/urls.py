from django.conf.urls import url

from .views import TypeformSyncView


urlpatterns = [
    url(r'(?P<typeform_uid>[0-9A-Za-z\-]+)/sync/', TypeformSyncView.as_view(), name='typeform_sync'),
]
