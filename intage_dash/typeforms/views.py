from django.http import HttpResponse
from django.views.generic import View

from .api import TypeformDataAPI
from .models import Typeform
from form_submissions.models import FormResponse


class TypeformSyncView(View):
    def get(self, request, typeform_uid):
        typeform = Typeform.objects.get(uid=typeform_uid)

        typeform_data_api = TypeformDataAPI()
        results = typeform_data_api.get_form_data(typeform.uid)

        typeform.payload = results
        typeform.save()

        for each in results['responses']:
            FormResponse.objects.create(
                typeform=typeform,
                answers=each['answers'],
                token=each['token']
            )

        return HttpResponse()
