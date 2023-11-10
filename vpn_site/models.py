from django.db import models
from django.contrib.auth.models import AbstractUser


class VPNUser(AbstractUser):
    image = models.ImageField(upload_to='images/profile/', blank=True, null=True)
    first_name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=50, null=True)


class Website(models.Model):
    user = models.ForeignKey(VPNUser, on_delete=models.CASCADE)
    site_link = models.CharField(unique=True)
    site_name = models.CharField(max_length=70, unique=True)


class VPNUserStatistics(models.Model):
    user = models.ForeignKey(VPNUser, on_delete=models.CASCADE)
    site = models.ForeignKey(Website, on_delete=models.CASCADE)

    pages_count = models.IntegerField(default=0)
    size_data_sent = models.FloatField(default=0)
    size_data_downloaded = models.FloatField(default=0)


    


