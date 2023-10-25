from django.db import models
from django.contrib.auth.models import AbstractUser, Group

# Create your models here.
class User(models.Model):
    #email = models.EmailField(unique=True, max_length=80)
    #groups = models.ManyToManyField(Group, related_name='None', blank=True)
    #USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['USERNAME']
    #full_name = models.CharField(max_length=100, blank=False)
    username = models.CharField(max_length=100, blank=False)
    password = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.username
