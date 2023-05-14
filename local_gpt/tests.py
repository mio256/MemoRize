from app import chatgpt_func
from django.test import TestCase
from django.http import JsonResponse
from django.template.response import TemplateResponse


class PingTestCase(TestCase):
    def testResponseType(self):
        response = self.client.get('/ping/')
        self.assertEqual(type(response), JsonResponse)

    def testResponseContent(self):
        response = self.client.get('/ping/')
        self.assertEqual(response.json(), {'result': True})


class IndexTestCase(TestCase):
    def testResponseType(self):
        response = self.client.get('/')
        self.assertEqual(type(response), TemplateResponse)


class ChatGPTTestCase(TestCase):
    def testSendUserContentResponseType(self):
        response = chatgpt_func.send_user_content('hello')
        content = response['choices'][0]['message']['content']
        self.assertEqual(type(content), str)
