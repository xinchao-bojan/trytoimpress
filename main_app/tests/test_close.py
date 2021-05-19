from .setup import TestSetUp
from main_app.models import Application


class Test(TestSetUp):
    route = '/api/application/close/'

    def test_anauthorized(self):
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 401)

    def test_user_without_applications(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'User dont have applications')

    def test_rate_closed(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        self.client.post(self.route)
        response = self.client.post(self.route)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Заявка уже закрыта')

    def test_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        response = self.client.post(self.route)
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.json().get('readystatus').get('status'), False)
