from django.db import models

class Game(models.Model):
    GENRE_CHOICES = [
        ('action', 'Action'),
        ('rpg', 'RPG'),
        ('strategy', 'Strategy'),
        ('sports', 'Sports'),
        ('indie', 'Indie'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    discount_price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='games/')
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    release_date = models.DateField()
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    @property
    def final_price(self):
        return self.discount_price if self.discount_price else self.price