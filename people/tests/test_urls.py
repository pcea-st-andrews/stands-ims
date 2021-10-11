from django.test import SimpleTestCase
from django.urls import resolve


class PeopleListURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "PeopleListView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:people_list")


class PersonCreateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/add/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "PersonCreateView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:person_create")


class PersonDetailURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/username/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "PersonDetailView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:person_detail")


class PersonUpdateURLTestCase(SimpleTestCase):
    def setUp(self):
        self.match = resolve("/people/username/update/")

    def test_view_func(self):
        self.assertEqual(self.match.func.__name__, "PersonUpdateView")

    def test_view_name(self):
        self.assertEqual(self.match.view_name, "people:person_update")