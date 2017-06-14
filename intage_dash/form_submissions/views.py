from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View


class ResponseWebhookView(View):
    @csrf_exempt
    def post(self, request):
        return HttpResponse()
