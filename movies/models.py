from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to='movie_images/')

    def __str__(self):
        return str(self.id) + ' - ' + self.name

    # ✅ NEW: calculate average rating for this movie
    def average_rating(self):
        avg = self.review_set.aggregate(Avg('rating'))['rating__avg']
        return round(avg, 1) if avg else 0


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    comment = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # ✅ NEW: numeric rating field (1–5 stars)
    rating = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('movie', 'user')  # each user can review once

    def __str__(self):
        return f'{self.id} - {self.movie.name} ({self.rating}/5)'
