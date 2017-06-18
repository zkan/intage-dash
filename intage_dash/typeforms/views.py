import copy

from django.http import HttpResponse
from django.views.generic import View

from .api import TypeformDataAPI
from .models import Typeform
from form_submissions.models import FormResponse


class TypeformSyncView(View):
    def _convert_rating_answers_to_integer(self, raw_answers):
        answers = copy.deepcopy(raw_answers)
        for each in answers:
            if 'rating_' in each:
                answers[each] = int(answers[each])

        return answers

    def get(self, request, typeform_uid):
        typeform = Typeform.objects.get(uid=typeform_uid)

        typeform_data_api = TypeformDataAPI()
        results = typeform_data_api.get_form_data(typeform.uid)

        typeform.payload = results
        typeform.save()

        for each in results['responses']:
            try:
                FormResponse.objects.get(token=each['token'])
            except FormResponse.DoesNotExist:
                answers = self._convert_rating_answers_to_integer(
                    each['answers']
                )
                if answers:
                    FormResponse.objects.create(
                        typeform=typeform,
                        answers=answers,
                        token=each['token']
                    )

        return HttpResponse()
