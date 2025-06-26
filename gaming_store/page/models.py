from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    genre = models.CharField(max_length=100)
    release_date = models.DateField(null=True, blank=True)     # NEW
    last_played = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
