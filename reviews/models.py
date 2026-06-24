from django.db import models
from users.models import User
from orders.models import Order

class Review(models.Model):

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='review'
    )

    client = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews'
    )

    prestataire = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='avis_recus'
    )

    note = models.IntegerField()  # 1 à 5
    commentaire = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.client.prenom} → {self.prestataire.prenom} : {self.note}/5"