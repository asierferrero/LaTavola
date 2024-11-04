from rest_framework import serializers
from .models import Produktua

class IkasleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Produktua
        fields = '__all__'