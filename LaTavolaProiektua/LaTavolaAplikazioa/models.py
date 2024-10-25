from django.contrib.auth.hashers import make_password
from django.db import models

class Erabiltzailea(models.Model):
    id = models.AutoField(primary_key=True)
    izena = models.CharField(max_length=100)
    abizena = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    pasahitza = models.CharField(max_length=128)
    jaiotze_data = models.DateField()
    helbidea = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.izena} {self.abizena}"

    def set_password(self, raw_password):
        self.pasahitza = make_password(raw_password)
        
class Hornitzailea(models.Model):
    id = models.AutoField(primary_key=True)
    izena = models.CharField(max_length=100)

    def __str__(self):
        return self.izena

class Langilea(models.Model):
    id = models.AutoField(primary_key=True)
    izena = models.CharField(max_length=100)
    abizena = models.CharField(max_length=100)
    postua = models.CharField(max_length=100)
    kontu_zenbakia = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.izena} {self.abizena}"

class Alergeno(models.Model):
    id = models.AutoField(primary_key=True)
    izena = models.CharField(max_length=100)

    def __str__(self):
        return self.izena

class Produktua(models.Model):
    id = models.AutoField(primary_key=True)
    izena = models.CharField(max_length=100)
    stock = models.IntegerField()
    hornitzaile = models.ForeignKey(Hornitzailea, on_delete=models.CASCADE)
    prezioa = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.izena

class AlergenoProduktua(models.Model):
    id = models.AutoField(primary_key=True)
    produktua = models.ForeignKey(Produktua, on_delete=models.CASCADE)
    alergeno = models.ForeignKey(Alergeno, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.produktua}{self.alergeno}"

class Eskaria(models.Model):
    id = models.AutoField(primary_key=True)
    erabiltzailea = models.ForeignKey(Erabiltzailea, on_delete=models.CASCADE)
    produktua = models.ForeignKey(Produktua, on_delete=models.CASCADE)
    langilea = models.ForeignKey(Langilea, on_delete=models.CASCADE)
    banatzailea = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}{self.erabiltzailea}"

class Iritzia(models.Model):
    id = models.AutoField(primary_key=True)
    erabiltzailea = models.ForeignKey(Erabiltzailea, on_delete=models.CASCADE)
    testua = models.TextField()
    izarrak = models.IntegerField()

    def __str__(self):
        return f"{self.erabiltzailea}{self.izarrak}"
