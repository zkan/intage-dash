import json

from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .models import FormResponse
from typeforms.models import Typeform


class ResponseWebhookView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResponseWebhookView, self).dispatch(*args, **kwargs)

    def _get_answers(self, payload):
        answers = {}
        for each in payload['form_response']['answers']:
            if each['field']['type'] == 'multiple_choice':
                key = 'list_' + each['field']['id'] + '_choice'
                value = each['choice']['label']
            elif each['field']['type'] == 'rating':
                key = 'rating_' + each['field']['id']
                value = each['number']
            answers[key] = value

        return answers

    def post(self, request):
        payload = json.loads(request.body)

        typeform = Typeform.objects.get(
            uid=payload['form_response']['form_id']
        )
        answers = self._get_answers(payload)

        FormResponse.objects.create(
            typeform=typeform,
            answers=answers,
            token=payload['form_response']['token']
        )

        return HttpResponse()
