import json
import time

import requests
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


class fastProxy(models.Model):
    proxiesText = models.TextField(null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        Proxy.objects.all().delete()
        for ip in self.proxiesText.splitlines():
            print(len(ip.split(':')))
            if len(ip.split(':')) == 4:
                auth = ip.split(':')[0]+':'+ip.split(':')[1]
                ip = ip.split(':')[2]+':'+ip.split(':')[3]
                ip = auth+'@'+ip
            # if try_proxy(ip):
            Proxy.objects.create(ip=ip)


class fastInstagramAccount(models.Model):
    accounts = models.TextField(null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        for acc in self.accounts.splitlines():
            Account.objects.create(username=acc.split(':')[0], password=acc.split(':')[1], client=self.client)


def try_proxy(proxy):
    headers = {
        'accept': "*/*",
        'accept-encoding': "gzip, deflate, br",
        'accept-language': "en-US,en;q=0.8",
        'content-length': "241",
        'content-type': 'application/x-www-form-urlencoded',
        'origin': "https://www.instagram.com",
        'referer': "https://www.instagram.com/",
        'user-agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36",
        'x-csrftoken': "95RtiLDyX9J6AcVz9jtUIySbwf75WhvG",
        'x-instagram-ajax': "c7e210fa2eb7",
        'x-requested-with': "XMLHttpRequest",
        'Cache-Control': "no-cache",
    }
    payload = {
        'email': 'testew32@mail.com',
        'password': 'testet',
        'username': 'Testuser',
        'first_name': 'Testuser',
        'client_id': 'W6mHTAAEAAHsVu2N0wGEChTQpTfn',
        'seamless_login_enabled': '1',
        'gdpr_s': '%5B0%2C2%2C0%2Cnull%5D',
        'tos_version': 'eu',
        'opt_into_one_tap': 'false'
    }
    proxies = {"http": "http://" + proxy, "https": "https://" + proxy}

    try:
        request = requests.post("https://www.instagram.com/accounts/web_create_ajax/", data=payload, proxies=proxies,
                                headers=headers)
        response = json.loads(request.text)
        try:
            if (response["account_created"] is False):
                if (response["errors"]["password"]):

                    print(response["errors"]["password"]["message"])
                    return False
                elif (response["errors"]["ip"]):
                    return False
                else:
                    return False
        except:
            return False
    except:
        return False
    return True


class Account(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    # image = models.ImageField(null=True, upload_to='shared_photos')
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.username


class Announcement(models.Model):
    status = models.BooleanField(default=False)
    message = models.TextField(default="")
    valid_date = models.DateField(null=True)

    def __str__(self):
        return self.message


class Post(models.Model):
    image = models.ImageField(null=True, upload_to='shared_photos')
    status = models.BooleanField(default=True)
    text = models.TextField(default='')
    client = models.OneToOneField(Client, on_delete=models.CASCADE, null=True)
    #
    # def save(self, **kwargs):
    #     img = Image.open(self.image.path)
    #     super().save()
    #     img.save(self.image.path)


class Proxy(models.Model):
    ip = models.CharField(max_length=25)

    def __str__(self):
        return self.ip
