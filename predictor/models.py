from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    alamat = models.TextField(max_length=100,blank=False)
    first_name = models.TextField(max_length=100,blank=False)
    birth_date = models.TextField(null=True,blank=True)


@receiver(post_save, sender=User)
def update_user_profile(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()