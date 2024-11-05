from rest_framework import serializers
from .models import Produktua, Alergeno

class AlergenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergeno
        fields = ['izena', 'img']
        
class ProduktuakSerializers(serializers.ModelSerializer):
    alergenoak = AlergenoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Produktua
        fields = '__all__'