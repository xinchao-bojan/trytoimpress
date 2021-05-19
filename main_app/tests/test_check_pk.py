from .setup import TestSetUp
from main_app.models import Application


class Test(TestSetUp):
    def route(self, pk):
        return f'/api/application/check/{pk}/'

    def close(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        self.client.post('/api/application/close/', {'status': 'lol'})

    def test_anauthorized(self):
        response = self.client.post(self.route(1), {'status': 'accepted'})

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.post(self.route(1), {'status': 'accepted'})

        self.assertEqual(response.status_code, 401)

    def test_not_existing_application(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.post(self.route(20), {'status': 'accepted'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Application does not exist')

    def test_not_existing_status(self):
        self.close()
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.post(self.route(1), {'status': 'lol'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Add correct status')

    def test_open_application(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        self.client.post(self.route(1), data={'status': 'accepted'})
        response = self.client.post(self.route(1), {'status': 'accepted'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Невозможно оценить открытую заявку')

    def test_valid_accepted(self):
        self.close()
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.post(self.route(1), {'status': 'accepted'})
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('accepted' in response.json().get('checkstatus_set'))

    def test_valid_rejected(self):
        self.close()
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.post(self.route(1), {'status': 'rejected'})
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('rejected' in response.json().get('checkstatus_set'))

    def test_valid_accepted(self):
        self.close()
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.post(self.route(1), {'status': 'revision'})
        self.assertEqual(response.status_code, 200)
        # self.assertTrue('revision' in response.json().get('checkstatus_set'))
