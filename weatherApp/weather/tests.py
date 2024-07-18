from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from weather.models import City

User = get_user_model()


class UserProfileTests(TestCase):

    def setUp(self):
        # Инициализация клиента API
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.city1 = City.objects.create(user=self.user, city_name='Paris', search_counter=5)
        self.city2 = City.objects.create(user=self.user, city_name='Berlin', search_counter=3)

    def test_create_profile_api(self):
        # Тест создания профиля пользователя через API
        data = {'username': 'newuser', 'email': 'newuser@example.com', 'password': 'newpassword'}
        response = self.client.post(reverse('create-profile'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'newuser@example.com')

    def test_city_creation(self):
        # Тест создания города в базе данных
        city = City.objects.create(user=self.user, city_name='London', search_counter=2)
        self.assertEqual(city.city_name, 'London')
        self.assertEqual(city.search_counter, 2)
        self.assertEqual(city.user.username, 'testuser')


class CityTests(TestCase):

    def setUp(self):
        # Инициализация тестовых данных
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')
        self.city1 = City.objects.create(user=self.user, city_name='Paris', search_counter=5)
        self.city2 = City.objects.create(user=self.user, city_name='Berlin', search_counter=3)

    def test_latest_profile_cities(self):
        # Тест получения последних поисковых городов для профиля пользователя
        self.client.force_login(self.user)
        response = self.client.get(reverse('latest_profile_cities', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        data = response.json()

        self.assertIn('cities', data)
        cities = data['cities']
        self.assertEqual(len(cities), 2)

        # Сортируем города по имени перед сравнением
        sorted_cities = sorted(cities, key=lambda x: x['city_name'])

        # Проверяем отсортированные города и их счетчики поиска
        self.assertEqual(sorted_cities[0]['city_name'], 'Berlin')
        self.assertEqual(sorted_cities[0]['search_count'], 3)
        self.assertEqual(sorted_cities[1]['city_name'], 'Paris')
        self.assertEqual(sorted_cities[1]['search_count'], 5)

    def test_get_weather(self):
        # Тест получения погоды для указанного города
        response = self.client.get(reverse('get_weather', kwargs={'city_name': 'Paris'}), data={'username': 'testuser'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_profile(self):
        # Тест создания профиля пользователя
        response = self.client.post(reverse('create-profile'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpassword',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
