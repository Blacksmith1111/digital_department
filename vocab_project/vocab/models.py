from django.db import models

class CardSet(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Card(models.Model):
    set = models.ForeignKey(CardSet, on_delete=models.CASCADE)
    term = models.CharField(max_length=200)
    definition = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)