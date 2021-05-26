from main_app.tests.setup import TestSetUp
from custom_user.models import CustomUser


class Test(TestSetUp):
    route = '/api/users/roles/'

    def test_anauthorized(self):
        response = self.client.put(self.route)

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.put(self.route)

        self.assertEqual(response.status_code, 401)

    def test_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.get(self.route)
        self.assertEqual(response.status_code, 200)
