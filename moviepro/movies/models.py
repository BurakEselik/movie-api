from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from decimal import Decimal
from django.db.models.signals import post_save
from django.dispatch import receiver
from scripts.rating import get_imdb_rating
from threading import Thread

class Movie(models.Model):
    name = models.CharField(max_length=214)
    director = models.CharField(max_length=214)
    subject = models.TextField(max_length=10000)
    release_date = models.DateField()
    imdb = models.DecimalField(max_digits=3,
                               decimal_places=1,
                               validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('10.0'))],
                               null=True,
                               blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.release_date}"

    def save(self, *args, **kwargs) -> None:
        if self.imdb is None:
            self.imdb = get_imdb_rating(self.name)
        super().save(*args, **kwargs)
