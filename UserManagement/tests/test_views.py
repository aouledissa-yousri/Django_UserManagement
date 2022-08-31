from django.test import TestCase
from django.urls import reverse, resolve


class TestViews(TestCase):


    def testLocationBasedLogin(self):
        print(reverse("location based login"))

