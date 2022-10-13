from statistics import mode
from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    address = models.CharField(max_length=250, default="Nalco colony")
    city = models.CharField(max_length=50, default="Bhubaneswar")
    state = models.CharField(max_length=50, default="Odisha")
    zip = models.IntegerField(default=751023)
    is_student = models.BooleanField(default=False)
    is_school_coordinator = models.BooleanField(default=False)
    vaccination_status = models.BooleanField(default=False)
    vaccination_date = models.CharField(max_length=10, default='08-10-2022')
    name_of_vaccination = models.CharField(max_length=20, default="covaxin")

class VaccinationDrive(models.Model):
    date = models.CharField(max_length=10, unique=True)
    no_of_slots = models.IntegerField()
    is_slote_done = models.BooleanField(default=False)

    def __str__(self):
        return self.date
