from .setup import TestSetUp
from main_app.models import Application


class Test(TestSetUp):
    route = '/api/application/create/'

    def test_anauthorized(self):
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 401)

    def test_without_data(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'KeyError')

    def test_valid(self):
        data = {
            'first_name': 'Maksim',
            'last_name': 'Garshin',
            'university': 'IT',
            'group': 'IVBO-05-19'
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        a1 = Application.objects.all().count()
        response = self.client.post(self.route, data)
        a2 = Application.objects.all().count()

        self.assertEqual(response.status_code, 201)
        self.assertEqual(a1 + 1, a2)
