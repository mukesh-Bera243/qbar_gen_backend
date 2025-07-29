from .models import *
from rest_framework import serializers

class QBarDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = QBarDetails
        fields = '__all__'