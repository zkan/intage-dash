from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class ResponseWebhookView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ResponseWebhookView, self).dispatch(*args, **kwargs)

    def post(self, request):
        return HttpResponse()
