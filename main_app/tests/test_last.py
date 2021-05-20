from .setup import TestSetUp
from main_app.models import ReadyStatus


class Test(TestSetUp):
    route = '/api/application/last/'

    def test_anauthorized(self):
        response = self.client.get(self.route)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.get(self.route)

        self.assertEqual(response.status_code, 401)

    def test_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        response = self.client.get(self.route)
        self.assertEqual(response.status_code, 200)
