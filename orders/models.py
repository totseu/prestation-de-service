from django.db import models
from users.models import User
from services.models import Service

class Order(models.Model):

    STATUT_CHOICES = [
        ('planifie', 'Planifié'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('annule', 'Annulé'),
    ]

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    statut = models.CharField(
        max_length=20,
        choices=STATUT_CHOICES,
        default='planifie'
    )

    avancement = models.IntegerField(default=0)  # 0 à 100
    date_reservation = models.DateTimeField(auto_now_add=True)
    date_livraison = models.DateField(null=True, blank=True)
    montant = models.DecimalField(max_digits=10, decimal_places=0)

    def __str__(self):
        return f"{self.client.prenom} → {self.service.titre}"