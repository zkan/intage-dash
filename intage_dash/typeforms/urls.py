from django.conf.urls import url

from .views import TypeformSyncView


urlpatterns = [
    url(r'sync/', TypeformSyncView.as_view(), name='typeform_sync'),
]
