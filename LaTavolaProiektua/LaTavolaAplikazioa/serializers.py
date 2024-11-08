from rest_framework import serializers
from .models import Produktua, Alergeno, T2Product


class AlergenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergeno
        fields = ['izena', 'img']
        
class ProduktuakSerializers(serializers.ModelSerializer):
    alergenoak = AlergenoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Produktua
        fields = '__all__'



#TODO terminar de verificar el modelo de BBDD dele grupo 2 y mirar si las funciones estan bien

class T2AlergenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergeno
        fields = ['izena', 'img']

class T2ProduktuakSerializer(serializers.ModelSerializer):
    alergenoak = T2AlergenoSerializer(many=True,read_only=True)

    class Meta:
        model = T2Product
        fields = '__all__'
