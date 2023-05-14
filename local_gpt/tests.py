from django.test import TestCase
from django.http import JsonResponse


class PingTestCase(TestCase):
    def testResponseType(self):
        response = self.client.get('/ping/')
        self.assertEqual(type(response), JsonResponse)

    def testResponseContent(self):
        response = self.client.get('/ping/')
        self.assertEqual(response.json(), {'result': True})
