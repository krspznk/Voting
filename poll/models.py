from django.db import models
from django.contrib.auth.models import User

# Модель квітів
class Flower(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

# Модель голосування
class Vote(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # ОНОВЛЕНО
    first_place = models.ForeignKey(Flower, related_name='first_place_votes', on_delete=models.CASCADE)
    second_place = models.ForeignKey(Flower, related_name='second_place_votes', on_delete=models.CASCADE)
    third_place = models.ForeignKey(Flower, related_name='third_place_votes', on_delete=models.CASCADE)

    def __str__(self):
        return f'Vote by {self.user.username}'
