from .setup import TestSetUp
from main_app.models import ReadyStatus


class Test(TestSetUp):
    route = '/api/application/close/all/'

    def test_anauthorized(self):
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 401)

    def test_wrong_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        response = self.client.get(self.route)
        self.assertEqual(response.status_code, 403)

    def test_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.post(self.route)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(ReadyStatus.objects.filter(status=True).count() == 0)
