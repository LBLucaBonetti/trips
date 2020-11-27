from django.core.exceptions import PermissionDenied
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.
from django.db.models.signals import pre_delete
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, first_name, last_name, password=None):
        if not email:
            raise ValueError("Email mancante")
        if not username:
            raise ValueError("Username mancante")
        if not first_name:
            raise ValueError("Nome mancante")
        if not last_name:
            raise ValueError("Cognome mancante")

        user = self.model(email=self.normalize_email(email), username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, first_name, last_name, password=None):
        user = self.create_user(email=email, username=username, first_name=first_name, last_name=last_name, password=password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser):
    class Meta:
        verbose_name = "Utente"
        verbose_name_plural = "Utenti"
    email = models.EmailField(verbose_name="Email", max_length=320, unique=True)
    username = models.CharField(verbose_name="Nome utente", max_length=255, unique=True)
    date_joined = models.DateTimeField(verbose_name="Data di registrazione", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="Ultimo login", auto_now=True)
    is_admin = models.BooleanField(verbose_name="Amministratore", default=False)
    is_active = models.BooleanField(verbose_name="Attivo", default=True)
    is_staff = models.BooleanField(verbose_name="Staff", default=False)
    is_superuser = models.BooleanField(verbose_name="Superutente", default=False)

    first_name = models.CharField(verbose_name="Nome", max_length=255)
    last_name = models.CharField(verbose_name="Cognome", max_length=255)
    phone_number = models.CharField(verbose_name="Numero di telefono", max_length=15, blank=True)
    birth_date = models.DateField(verbose_name="Data di nascita", blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email + " - " + self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return True


@receiver(pre_delete, sender=CustomUser)
def prevent_superuser_deletion(sender, instance, **kwargs):
    if instance.is_superuser:
        raise PermissionDenied
