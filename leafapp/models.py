from django.db import models

# Create your models here.
class Users(models.Model):
    Name=models.CharField(max_length=30)
    EmailID=models.CharField(max_length=30)
    Password=models.CharField(max_length=30)
    PhoneNo=models.BigIntegerField()
class Discussion(models.Model):
    Name=models.CharField(max_length=30)
    Experience=models.TextField()
class Feedback(models.Model):
    Name=models.CharField(max_length=30)
    Condition=models.CharField(max_length=30)
    Accurancy=models.CharField(max_length=30)