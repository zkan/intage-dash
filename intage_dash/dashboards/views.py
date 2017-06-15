from django.shortcuts import render
from django.views.generic import TemplateView


class DashboardView(TemplateView):
    template_name = 'dashboard.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
        )
