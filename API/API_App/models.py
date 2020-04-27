from django.db import models

# Create your models here.


class EmployeeData(models.Model):

    eno = models.IntegerField(null=True)
    ename = models.CharField(max_length=500, null=True)
    esal = models.IntegerField(null=True)
    eaddr = models.CharField(max_length=500, null=True)
