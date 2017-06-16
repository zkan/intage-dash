from django.conf.urls import url

from .views import DashboardView


urlpatterns = [
    url(r'(?P<typeform_uid>[0-9A-Za-z\-]+)/',
        DashboardView.as_view(), name='dashboard'),
]
