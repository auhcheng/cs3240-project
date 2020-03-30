from django.test import TestCase
from .views import get_weather_context

class DashboardTests(TestCase):

    def test_weather_is_consistent(self):
        context1 = get_weather_context()
        context2 = get_weather_context()

        self.assertEqual(context1, context2)
    
    def test_weather_context_is_dict(self):
        context = get_weather_context()
        self.assertIsInstance(context, dict)
    
    def test_weather_city_is_Charlottesville(self):
        city_weather = get_weather_context()['city_weather']
        self.assertEqual(city_weather['city'], 'Charlottesville')
    
    def test_weather_temperature_is_number(self):
        city_weather = get_weather_context()['city_weather']
        self.assertIsInstance(city_weather['temperature'], float)
    
    def test_weather_description_is_string(self):
        city_weather = get_weather_context()['city_weather']
        self.assertIsInstance(city_weather['description'], str)