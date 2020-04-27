from django.db import models

# Create your models here.


class Employee(models.Model):

    eno = models.IntegerField(null=True)
    ename = models.CharField(max_length=200, null=True)
    esal = models.CharField(max_length=200, null=True)
    eaddr = models.TextField(max_length=500, null=True)
