from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32)
    psw = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

class Preference(models.Model):
    username = models.CharField(max_length=32)
    pub_date = models.DateTimeField('date published')
    choice = models.IntegerField(default=0)
    remark = models.CharField(max_length=200)