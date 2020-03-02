from django.test import TestCase
from .views import get_weather_context

class DashboardTests(TestCase):

    def test_weather_is_consistent(self):
        context1 = get_weather_context()
        context2 = get_weather_context()

        self.assertEqual(context1, context2)