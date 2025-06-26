from django.db import models

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255, default='Unknown')
    release_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='games/', blank=True, null=True)  # This is important

    def __str__(self):
        return self.title
