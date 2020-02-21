from django.db import models
from django.utils import timezone

# Create your models here.

class User(models.Model):
    userid = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=10)
    age = models.IntegerField()
    hobby = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.userid}/{self.name}/{self.age}/{self.hobby}"

class Image(models.Model):
    author = models.ForeignKey('auth.user', on_delete=models.CASCADE)
    filename = models.CharField(max_length=50)