from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("L'email est obligatoire")

        email = self.normalize_email(email)

        user = self.model(
            email=email,
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user


    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(
            email,
            password,
            **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):

    ROLE_CHOICES = [
        ('client', 'Client'),
        ('prestataire', 'Prestataire'),
    ]


    SEXE_CHOICES = [
        ('Homme','Homme'),
        ('Femme','Femme'),
    ]


    email = models.EmailField(unique=True)

    nom = models.CharField(max_length=100)

    prenom = models.CharField(max_length=100)

    age = models.IntegerField()

    sexe = models.CharField(
        max_length=10,
        choices=SEXE_CHOICES
    )


    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        null=True,
        blank=True
)

    photo_profil = models.ImageField(
        upload_to="profils/",
        null=True,
        blank=True
    )


    photo_cni = models.ImageField(
        upload_to="cni/",
        null=True,
        blank=True
    )


    certificat = models.ImageField(
        upload_to="certificats/",
        null=True,
        blank=True
    )


    fonction = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )


    is_active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)


    objects = UserManager()


    USERNAME_FIELD = 'email'


    REQUIRED_FIELDS = [
        'nom',
        'prenom',
        'age',
        'sexe',
    ]


    def __str__(self):
        return self.email