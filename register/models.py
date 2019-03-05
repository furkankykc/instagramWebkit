from django.contrib.auth.models import User
from django.db import models
from PIL import Image


# Create your models here.


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.IntegerField()
    status = models.BooleanField(default=True)
    email = models.EmailField(null=True)
    # password = models.CharField(max_length=20)
    isim = models.CharField(max_length=20)
    # isAdmin = models.BooleanField(default=True)
    # accounts = models.ManyToManyField(Account)
    maxAccountCount = models.IntegerField(default=100)
    mobile_number = models.CharField(max_length=11)
    credit = models.IntegerField(default=1000)

    def __str__(self):
        return self.isim

class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    image = models.ImageField(null=True, upload_to='shared_photos')
    client = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username

class Announcement(models.Model):
    status = models.BooleanField(default=False)
    message = models.TextField(default="")
    valid_date = models.DateField(null=True)


    def __str__(self):
        return self.message
class Post(models.Model):
    image = models.ImageField(null=True,upload_to='shared_photos')
    status = models.BooleanField(default=True)
    text = models.TextField(default='')
    client = models.OneToOneField(Client,on_delete=models.CASCADE ,null=True)
    #
    # def save(self, **kwargs):
    #     img = Image.open(self.image.path)
    #     super().save()
    #     img.save(self.image.path)


class Proxy(models.Model):
    ip = models.CharField(max_length=25)

    def __str__(self):
        return self.ip