from django.http import HttpResponse
from django.views.generic import View


class TypeformSyncView(View):
    def get(self, request):
        return HttpResponse()
