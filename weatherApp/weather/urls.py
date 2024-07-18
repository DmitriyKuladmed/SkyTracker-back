from django.urls import path
from .views import UserProfileView, UserLoginView, WeatherView, LatestCitiesView, LatestCitiesProfileView

urlpatterns = [
    path('create-profile/', UserProfileView.as_view(), name='create-profile'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('get-weather/<str:city_name>/', WeatherView.as_view(), name='get_weather'),
    path('latest-cities/<str:username>/', LatestCitiesView.as_view(), name='latest_cities'),
    path('latest-profile-cities/<str:username>/', LatestCitiesProfileView.as_view(), name='latest_profile_cities'),
]
