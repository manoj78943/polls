from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Questions(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_at = models.DateTimeField(auto_now=True)
    question = models.CharField(max_length=500)
    first_option = models.CharField(max_length=100)
    second_option = models.CharField(max_length=100)
    third_option = models.CharField(max_length=100)
    fourth_option = models.CharField(max_length=100)


class Answers(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answers = models.CharField(max_length=100)
    
class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.IntegerField()
