from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal


class Movie(models.Model):
    name = models.CharField(max_length=214)
    director = models.CharField(max_length=214)
    subject = models.TextField(max_length=10000)
    release_date = models.DateField()
    imdb = models.DecimalField(max_digits=3,
                               decimal_places=1,
                               validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('10.0'))])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.release_date}"
