from django.conf.urls import url

from .views import ResponseWebhookView


urlpatterns = [
    url(r'webhook/',
        ResponseWebhookView.as_view(), name='submission_webhook'),
]
