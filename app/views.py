from django.http import JsonResponse
from django.views.generic import TemplateView


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "app/index.html"
