from main_app.tests.setup import TestSetUp
from custom_user.models import CustomUser


class Test(TestSetUp):
    route = '/api/users/addposition/'

    def test_anauthorized(self):
        response = self.client.put(self.route, {'status': 'accepted'})

        self.assertEqual(response.status_code, 401)

    def test_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='lol_kek')
        response = self.client.put(self.route, {'status': 'accepted'})

        self.assertEqual(response.status_code, 401)

    def test_wrong_permission(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        response = self.client.get(self.route, {'user': 'auth0.60929d2255c45f00681ec4d1', 'position': 'headboy'})
        self.assertEqual(response.status_code, 403)

    def test_invalid_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.put(self.route, {'user': 'invalid', 'position': 'headboy'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Custom user does not exist')

    def test_invalid_user_type(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.put(self.route, {'user': True, 'position': True})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Custom user does not exist')

    def test_invalid_position_type(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.put(self.route, {'user': 'auth0.60929d2255c45f00681ec4d1', 'position': True})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Custom user does not exist')

    def test_without_pos(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.put(self.route, {'user': 'invalid'})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'KeyError')

    def test_without_user(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.put(self.route, {'position': 'headboy'})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'KeyError')

    def test_valid_get(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.get(self.route)

        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.json().get('results')) > 0)

    def test_valid_put(self):
        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        response = self.client.put(self.route, {'user': 'auth0.60929d2255c45f00681ec4d1', 'position': 'headboy'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(CustomUser.objects.get(name='auth0.60929d2255c45f00681ec4d1').position.last().position,
                         'headboy')
