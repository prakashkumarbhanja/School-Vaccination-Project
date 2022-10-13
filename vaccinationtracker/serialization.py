from django.db.models import fields
from rest_framework import serializers

from vaccinationtracker.models import *

class CustomUserSerialization(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = '__all__'

class VaccinationDriveSerialization(serializers.ModelSerializer):
    class Meta:
        model = VaccinationDrive
        fields = '__all__'