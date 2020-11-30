import datetime

import django
from django.contrib.auth import get_user_model, logout
from django.core.exceptions import PermissionDenied
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import CustomUser

# Create your tests here.


class UsersTestCase(TestCase):
    def setUp(self):
        CustomUser.objects.create(
            email="prova1@prova.com",
            username="prova1",
            first_name="prova1",
            last_name="prova1",
            password="passuord"
        )
        CustomUser.objects.create(
            email="prova2@prova.com",
            username="prova2",
            first_name="prova2",
            last_name="prova2",
            password="passuord"
        )
        CustomUser.objects.create(
            email="admin@admin.com",
            username="admin",
            first_name="admin",
            last_name="admin",
            is_superuser=True,
            password="password123!"
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

    def test_cannot_have_two_users_with_same_username_or_email(self):
        try:
            with transaction.atomic():
                u = CustomUser.objects.create(
                    email="prova1@prova.com",
                    username="prova1",
                    first_name="prova1",
                    last_name="prova1",
                )
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                u = CustomUser.objects.create(
                    email="prova1@prova.com",
                    username="prova3",
                    first_name="prova3",
                    last_name="prova3",
                )
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                u = CustomUser.objects.create(
                    email="prova1@prova.com",
                    username="prova3",
                    first_name="prova3",
                    last_name="prova3",
                )
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                u = CustomUser.objects.create(
                    email="prova3@prova.com",
                    username="prova1",
                    first_name="prova3",
                    last_name="prova3",
                )
        except IntegrityError:
            pass

        try:
            with transaction.atomic():
                u = CustomUser.objects.create(
                    email="prova6@prova.com",
                    username="prova6",
                    first_name="prova1",
                    last_name="prova1",
                )
        except IntegrityError:
            self.fail("Two users sharing only the same first and last name could not be stored")

    def test_can_have_two_users_with_same_first_and_last_name(self):
        u = CustomUser.objects.create(
            email="prova4@prova.com",
            username="prova4",
            first_name="prova4",
            last_name="prova4",
        )
        try:
            u = CustomUser.objects.create(
                email="prova5@prova.com",
                username="prova5",
                first_name="prova4",
                last_name="prova4",
            )
        except IntegrityError:
            return False

    def test_users_can_register(self):
        response = self.client.post(reverse("user_register"), data={
            "email": "pippo@pippo.com",
            "username": "pippo",
            "first_name": "pippo",
            "last_name": "pippo",
            "password1": "passuord",
            "password2": "passuord"
        })

        users = get_user_model().objects.filter(email="pippo@pippo.com", username="pippo", first_name="pippo", last_name="pippo")
        self.assertTrue(users)

    def test_users_can_login(self):
        response = self.client.post(reverse("user_login"), data={
            "username": "prova1@prova.com",
            "password": "passuord"
        })
        prova1 = CustomUser.objects.filter(email="prova1@prova.com").get()
        self.assertTrue(prova1.is_authenticated)

        response = self.client.post(reverse("user_login"), data={
            "username": "admin@admin.com",
            "password": "password123!"
        })
        admin = CustomUser.objects.filter(email="admin@admin.com").get()
        self.assertTrue(admin.is_authenticated)

    def test_users_can_logout_after_login(self):
        response = self.client.post(reverse("user_login"), data={
            "username": "prova1@prova.com",
            "password": "passuord"
        })
        prova1 = CustomUser.objects.filter(email="prova1@prova.com").get()
        self.assertTrue(prova1.is_authenticated)
        response = self.client.post(reverse("user_logout"))
        self.assertFalse(prova1.is_authenticated)
