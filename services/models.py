from django.db import models

# Create your models here.
from django.db import models
from users.models import User

class Service(models.Model):

    CATEGORIE_CHOICES = [
        ('dev_web', 'Développement Web'),
        ('design', 'Design Graphique'),
        ('marketing', 'Marketing Digital'),
        ('traduction', 'Traduction'),
        ('redaction', 'Rédaction'),
        ('conseil', 'Conseil'),
    ]

    prestataire = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='services'
    )

    titre = models.CharField(max_length=200)
    description = models.TextField()
    categorie = models.CharField(max_length=50, choices=CATEGORIE_CHOICES)
    prix = models.DecimalField(max_digits=10, decimal_places=0)
    disponible = models.BooleanField(default=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} — {self.prestataire.prenom}"