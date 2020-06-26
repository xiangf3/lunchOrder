from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=32)
    psw = models.CharField(max_length=128)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    def __str__(self):
        return self.username

class Preference(models.Model):
    username = models.CharField(max_length=32)
    pub_date = models.DateTimeField('date published')
    choice = models.CharField(max_length=32)
    remark = models.CharField(max_length=200)
    budget = models.IntegerField(default=0)
    def __str__(self):
        return self.choice