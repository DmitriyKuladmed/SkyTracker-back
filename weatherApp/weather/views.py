import requests
import os

from dotenv import load_dotenv
from googletrans import Translator

from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView

from django.views.generic import TemplateView, FormView, View
from django.contrib.auth import authenticate, get_user_model
from django.shortcuts import render
from django.http import JsonResponse
from django.urls import reverse_lazy

from .models import City, UserProfile
from .serializers import UserProfileSerializer

load_dotenv()
User = get_user_model()


class UserProfileView(generics.CreateAPIView):
    """
    API view для создания профиля пользователя.
    Принимает данные пользователя, валидирует и сохраняет профиль.
    """

    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

    def post(self, request, *args, **kwargs):
        """
        Обработчик POST запроса для создания профиля пользователя.
        """

        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    API view для аутентификации пользователя.
    Принимает имя пользователя и пароль, проверяет их и возвращает профиль пользователя в случае успеха.
    """

    def post(self, request):
        """
        Обработчик POST запроса для аутентификации пользователя.
        """

        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            serializer = UserProfileSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)


class WeatherView(View):
    """
    View для получения погоды для указанного города.
    Использует внешний API для получения данных о погоде и переводит описание погоды на русский язык.
    """

    def get_weather(self, city_name):
        """
        Получает данные о погоде для указанного города.
        """

        url = os.getenv('WEATHER_URL')
        response = requests.get(url.format(city_name)).json()

        original_description = response['weather'][0]['description']
        translator = Translator()
        translated_description = translator.translate(original_description, src='en', dest='ru').text

        weather_data = {
            'city': city_name,
            'temp': response['main']['temp'],
            'icon': response['weather'][0]['icon'],
            'wind': response['wind']['speed'],
            'description': translated_description
        }

        return weather_data

    def get(self, request, *args, **kwargs):
        """
        Обработчик GET запроса для получения данных о погоде.
        """

        city_name = kwargs.get('city_name')
        username = request.GET.get('username')

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        if not user.is_authenticated:
            return JsonResponse({'error': 'Unauthorized'}, status=401)

        city_instance, created = City.objects.get_or_create(
            user=user,
            city_name=city_name,
            defaults={'search_counter': 1}
        )

        if not created:
            city_instance.search_counter += 1
            city_instance.save()

        city_weather = self.get_weather(city_name)
        return JsonResponse(city_weather)


class LatestCitiesView(View):
    """
    View для получения списка последних просмотренных городов.
    Возвращает список названий городов, отсортированных по времени последнего просмотра.
    """

    def get(self, request, *args, **kwargs):
        """
        Обработчик GET запроса для получения списка последних просмотренных городов.
        """

        username = kwargs.get('username')
        user = User.objects.get(username=username)
        latest_cities = City.objects.filter(user=user.id).order_by('-last_searched')[:5]
        latest_cities_names = [city.city_name for city in latest_cities]

        return JsonResponse({'latest_cities': latest_cities_names})


class LatestCitiesProfileView(View):
    """
    View для получения списка последних просмотренных городов для указанного пользователя.
    Возвращает список городов и количество их просмотров, отсортированных по времени последнего просмотра.
    """

    def get(self, request, username):
        """
        Обработчик GET запроса для получения списка последних просмотренных городов пользователя.
        """

        cities = City.objects.filter(user__username=username).order_by('-last_searched')
        data = [
            {
                'city_name': city.city_name,
                'search_count': city.search_counter
            }
            for city in cities
        ]
        return JsonResponse({'cities': data})
