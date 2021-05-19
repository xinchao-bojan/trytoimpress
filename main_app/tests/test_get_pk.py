from .setup import TestSetUp
from main_app.models import Application


class Test(TestSetUp):
    def route(self, pk):
        return f'/api/application/get/{pk}/'

    def test_anauthorized(self):
        response = self.client.get(self.route(1))

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.get(self.route(1))

        self.assertEqual(response.status_code, 401)

    def test_discrepancy_between_user_and_id(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.get(self.route(1))

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Application does not exist')

    def test_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        a1 = Application.objects.first()
        response = self.client.get(self.route(1))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(a1.id, response.json().get('id'))
