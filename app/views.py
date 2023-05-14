from . import chatgpt_func
from django.http import JsonResponse
from django.views.generic import TemplateView


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "app/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        message = 'hello'
        gpt_response = chatgpt_func.send_user_content(message)
        context['gpt_response'] = gpt_response['choices'][0]['message']['content']

        return context
