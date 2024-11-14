from rest_framework import serializers
from .models import Produktua, Alergeno, T2Product,Eskaria,Langilea


class AlergenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergeno
        fields = ['izena', 'img']
        
class ProduktuakSerializers(serializers.ModelSerializer):
    alergenoak = AlergenoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Produktua
        fields = '__all__'

class LangileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Langilea
        fields = '__all__'

class EskariaSerializer(serializers.ModelSerializer):

    langileak = LangileSerializer(many=True,read_only=True)
    produktuak = ProduktuakSerializers(many=True, read_only=True)

    class Meta:
        model = Eskaria
        fields = '__all__'


#TODO terminar de verificar el modelo de BBDD del grupo 2 y mirar si las funciones estan bien

class T2AlergenoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alergeno
        fields = ['izena', 'img']

class T2ProduktuakSerializer(serializers.ModelSerializer):
    alergenoak = T2AlergenoSerializer(many=True,read_only=True)

    class Meta:
        model = T2Product
        fields = '__all__'
