import datetime

from django.core.exceptions import PermissionDenied
from django.test import TestCase
from .models import CustomUser

# Create your tests here.


class UsersTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            email="prova1@prova.com",
            username="prova1",
            first_name="prova1",
            last_name="prova1",
        )
        CustomUser.objects.create(
            email="prova2@prova.com",
            username="prova2",
            first_name="prova2",
            last_name="prova2"
        )
        CustomUser.objects.create(
            email="admin@admin.com",
            username="admin",
            first_name="admin",
            last_name="admin",
            is_superuser=True
        )

    def test_superusers_cannot_be_deleted(self):
        try:
            CustomUser.objects.filter(email="admin@admin.com").delete()
        except PermissionDenied:
            return True

    def test_users_can_be_deleted(self):
        prova1 = CustomUser.objects.filter(email="prova1@prova.com")
        prova1.delete()
        self.assertFalse(prova1.exists())

    def test_users_can_modify_options(self):
        prova2 = CustomUser.objects.filter(email="prova2@prova.com")
        prova2 = prova2.get()
        prova2.first_name = "Prova2First"
        prova2.last_name = "Prova2Last"
        prova2.phone_number = "111111111111111"
        birthday = datetime.date.today()
        prova2.birth_date = birthday
        prova2.save()
        prova2 = CustomUser.objects.filter(email="prova2@prova.com")
        prova2 = prova2.get()
        self.assertEquals(prova2.first_name, "Prova2First")
        self.assertEquals(prova2.last_name, "Prova2Last")
        self.assertEquals(prova2.phone_number, "111111111111111")
        self.assertEquals(prova2.birth_date, birthday)
