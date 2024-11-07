from django.db import models
from django.contrib.auth.models import BaseUserManager, User

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        username = self.normalize_email(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, password, **extra_fields)

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
    img = models.ImageField(upload_to='LaTavolaAplikazioa/static/img',null=True, blank=True)

    def __str__(self):
        return self.izena

class Produktua(models.Model):
    HASIERAKOA = 'hasierakoa'
    LEHENA = 'lehena'
    BIGARRENA = 'bigarrena'
    GEHIGARRIA = 'gehigarria'
    POSTREA = 'postrea'
    KAFEA = 'kafea'

    MOTA_CHOICES = [
        (HASIERAKOA, 'Hasierakoa'),
        (LEHENA, 'Lehena'),
        (BIGARRENA, 'Bigarrena'),
        (GEHIGARRIA, 'Gehigarria'),
        (POSTREA, 'Postrea'),
        (KAFEA, 'Kafea'),
    ]
    
    id = models.AutoField(primary_key=True)
    izena = models.CharField(max_length=100)
    deskripzioa = models.CharField(max_length=300, null=True)
    alergenoak = models.ManyToManyField(Alergeno)
    img = models.ImageField(upload_to='LaTavolaAplikazioa/static/img',null=True, blank=True)
    prezioa = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    mota = models.CharField(max_length=100, choices=MOTA_CHOICES, null=True)
    adin_nagusikoa = models.BooleanField(default=False)

    def __str__(self):
        return self.izena

class Eskaria(models.Model):
    id = models.AutoField(primary_key=True)
    erabiltzailea = models.ForeignKey(User, on_delete=models.CASCADE)
    produktua = models.ForeignKey(Produktua, on_delete=models.CASCADE)
    langilea = models.ForeignKey(Langilea, on_delete=models.CASCADE)
    banatzailea = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id}{self.erabiltzailea}"

class Iritzia(models.Model):
    id = models.AutoField(primary_key=True)
    erabiltzailea = models.ForeignKey(User, on_delete=models.CASCADE)
    testua = models.TextField()
    izarrak = models.IntegerField()

    def __str__(self):
        return f"{self.erabiltzailea}{self.izarrak}"
