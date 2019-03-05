from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from register.restAPI.requestbot import runBot
from .models import *
from register.instaRest import InstagramClient


# Create your views here.
def auth(email, password):
    user = User.objects.filter(email=email).first()
    print(user.username)
    if user is not None:
        if user.password == password:
            return user
    return None


@login_required
def dashboard(request):
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'index.html', context)


@login_required
def follow(request):
    if request.method == 'POST':
        if rmcredit(request.user.username, 1):
            instaFollow(request.user.username, request.POST['username'])
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'followPage.html', context)


def rmcredit(user, ammount):
    client = Client.objects.get(user=User.objects.get(username=user))
    print(client.credit)
    cred = client.credit
    if cred-ammount >=0:
        client.credit=cred-ammount
        print('this it')
        return True
    else:
        return False


@login_required
def createuser(request):
    if request.method == 'POST':
        print('Count:', request.POST['count'])
        if rmcredit(request.user.username,1):
            instaCreate(request.user.username, request.POST['count'])
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'createUser.html', context)


@login_required
def comment(request):
    if request.method == 'POST':
        if rmcredit(request.user.username, 1):
            print('ttt')
            instaComment(request.user.username, request.POST['hf-link'], request.POST['hf-text'])
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'comment.html', context)


def instaPost(user):
    try:
        print('insta login ', user)
        user = Client.objects.get(user=User.objects.get(username=user))

        for acc in Account.objects.filter(client=user):
            instaCli = InstagramClient(acc.username, acc.password)
            instaCli.upload(Post.objects.filter(client=user, status=True))
    except:
        pass


def instaFollow(user, someone):
    print('insta login ', user)
    try:
        user = Client.objects.get(user=User.objects.get(username=user))

        for acc in Account.objects.filter(client=user):
            instaCli = InstagramClient(acc.username, acc.password)
            instaCli.followSomeOne(instaCli.get_user_id(someone))
    except:
        pass


def instaComment(user, media, text):
    print('insta login ', user)
    try:
        user = Client.objects.get(user=User.objects.get(username=user))

        for acc in Account.objects.filter(client=user):
            instaCli = InstagramClient(acc.username, acc.password)
            instaCli.api.comment(instaCli.get_media_id(media), text)
    except:
        pass

def instaCreate(user, count):
    print('running bot for ', user, count)
    if count is None:
        count=1
    runBot(user, count)


@login_required
def post(request):
    from .forms import PostUptadeForm
    if request.method == 'POST':
        forms = PostUptadeForm(request.POST, request.FILES)
        if forms.is_valid():
            forms.save()
        if rmcredit(request.user.username, 1):
            instaPost(request.user.username)


    else:
        forms = PostUptadeForm()

    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    post = Post(client=user)
    forms.fields['client'].initial = user
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts,

               'form': forms}
    return render(request, 'postPage.html', context)
