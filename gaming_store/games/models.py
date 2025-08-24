from django.db import models
from django.conf import settings # Import the settings to get the AUTH_USER_MODEL

class Game(models.Model):
    """
    Represents a game in the store.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    author = models.CharField(max_length=255, default='Unknown')
    release_date = models.DateField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='games/', blank=True, null=True)
    trailer_url = models.URLField(blank=True, null=True) # Assuming you have a trailer URL

    def __str__(self):
        return self.title


class Cart(models.Model):
    """
    Represents a user's shopping cart.
    A user has only one cart.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    """
    Represents a single game within a user's cart.
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.game.title} in {self.cart.user.username}'s cart"

    @property
    def total_price(self):
        return self.quantity * self.game.price
