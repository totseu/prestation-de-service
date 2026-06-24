from django.db import models
from users.models import User
from orders.models import Order

class Payment(models.Model):

    MODE_CHOICES = [
        ('orange', 'Orange Money'),
        ('mtn', 'MTN Mobile Money'),
        ('carte', 'Carte bancaire'),
    ]

    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('paye', 'Payé'),
        ('annule', 'Annulé'),
        ('rembourse', 'Remboursé'),
    ]

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='payments'
    )

    montant = models.DecimalField(max_digits=10, decimal_places=0)
    frais_plateforme = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    montant_total = models.DecimalField(max_digits=10, decimal_places=0, default=0)
    mode = models.CharField(max_length=20, choices=MODE_CHOICES, default='orange')
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    numero = models.CharField(max_length=20, blank=True)
    date_paiement = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Calcule automatiquement les frais (5%) et le total
        self.frais_plateforme = int(self.montant * 5 / 100)
        self.montant_total = self.montant + self.frais_plateforme
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Paiement {self.montant_total} FCFA — {self.order}"