import time

from rest_framework.test import APITestCase
import requests

from custom_user.models import CustomUser, Position

tokens = {}


class TestSetUp(APITestCase):
    ADMIN = ''
    STUDENT = ''

    def setUp(self):
        TestSetUp.STUDENT = self.get_token(username='student@mirea.ru', password='123')
        TestSetUp.ADMIN = self.get_token(username='director@mirea.ru', password='123')
        data = {
            'first_name': 'Maksudbek',
            'last_name': 'Igamberdyev',
            'university': 'IT',
            'group': 'IVBO-07-19'
        }
        self.client.credentials(HTTP_AUTHORIZATION=self.STUDENT)
        self.client.post('/api/application/create/', data)

        self.client.credentials(HTTP_AUTHORIZATION=self.ADMIN)
        self.client.get('/api/users/private/')
        p1 = Position.objects.create(position='student')
        p2 = Position.objects.create(position='director')
        c = CustomUser.objects.all().get(id=1)
        c.position.add(p1)
        c = CustomUser.objects.all().get(id=2)
        c.position.add(p2)
        c.is_staff = True
        c.save()
        self.client.credentials(HTTP_AUTHORIZATION='')
        return super().setUp()

    def get_token(self, username, password):
        global tokens

        if username in tokens:
            return tokens[username]

        r = requests.post('https://suroegin503.eu.auth0.com/oauth/token', data={
            'grant_type': 'password',
            'username': username,
            'password': password,
            'scope': 'openid profile email',
            'audience': 'https://welcome/',
            'client_id': 'PdkS09Ig0EYVGK9KPYwncjKMGzXnAasI'})

        tokens[username] = f"Bearer {r.json().get('access_token')}"
        return tokens[username]
