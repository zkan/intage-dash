from django.http import HttpResponse
from django.views.generic import View

from .api import TypeformDataAPI
from .models import Typeform


class TypeformSyncView(View):
    def get(self, request, typeform_uid):
        typeform = Typeform.objects.get(uid=typeform_uid)

        typeform_data_api = TypeformDataAPI()
        typeform_data_api.get_form_data(typeform.uid)

        return HttpResponse()
