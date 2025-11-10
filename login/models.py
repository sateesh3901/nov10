from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(primary_key=True, max_length= 60, null=False)
    password = models.CharField(max_length=150, null=False)