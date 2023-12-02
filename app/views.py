from . import chatgpt_func, gcal_func
from django.http import JsonResponse
from django.views.generic import TemplateView


def PingView(request):
    return JsonResponse({'result': True})


class IndexView(TemplateView):
    template_name = "app/index.html"

    def post(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        message = self.request.POST.get('next_message', 'hello')
        context['your_message'] = message
        gpt_response = chatgpt_func.send_user_content(message)
        context['gpt_response'] = gpt_response['choices'][0]['message']['content']

        return context


def calendar_view(request):
    processed_events = gcal_func.response_django()
    return JsonResponse(processed_events)
