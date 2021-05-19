from .setup import TestSetUp
from main_app.models import Application


class Test(TestSetUp):
    route = '/api/application/get/closed/'

    def close_application(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        self.client.post('/api/application/close/', {'status': 'lol'})

    def test_anauthorized(self):
        response = self.client.get(self.route)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.get(self.route)

        self.assertEqual(response.status_code, 401)

    def test_wrong_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        response = self.client.get(self.route)
        self.assertEqual(response.status_code, 403)

    def test_valid(self):
        self.close_application()
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.get(self.route)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json().get('results')) > 0)
