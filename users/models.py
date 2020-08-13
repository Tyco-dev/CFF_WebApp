from django.db import models
from django.contrib.auth.models import User
from phone_field import PhoneField
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.


class Company(models.Model):
    name = models.CharField(max_length=100, default='CFF')

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    phone_number = PhoneField()

    def __str__(self):
        return f'{self.user.username} Profile'


def create_profile(sender, instance, created, *args, **kwargs):
    # ignore if this is an existing User
    if not created:
        return
    Profile.objects.create(user=instance)


post_save.connect(create_profile, sender=User)
