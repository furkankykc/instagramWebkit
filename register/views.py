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
        count = request.POST['count']
        if rmcredit(request.user.username, count):
            instaFollow(request.user.username, request.POST['username'],count)
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'followPage.html', context)


def rmcredit(user, ammount):
    client = Client.objects.get(user=User.objects.get(username=user))
    print(client.credit)
    cred = int(client.credit)
    ammount = int(ammount)
    try:
        if int(cred - int(ammount)) >= 0:
            client.credit = cred - ammount
            print('this it')
            client.save()
            return True
        else:
            return False
    except:
        return False


@login_required
def createuser(request):
    if request.method == 'POST':
        print('Count:', request.POST['count'])
        count = request.POST['count']
        if rmcredit(request.user.username, count):
            instaCreate(request.user.username, count)
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'createUser.html', context)


@login_required
def comment(request):
    if request.method == 'POST':
        count = request.POST['hf-count']
        if rmcredit(request.user.username, count):
            print('ttt')
            instaComment(request.user.username, request.POST['hf-link'], request.POST['hf-text'],
                         count)
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'comment.html', context)


@login_required
def like(request):
    if request.method == 'POST':
        count = request.POST['count']
        if rmcredit(request.user.username, count):
            print('ttt', request.POST['count'])
            instaLike(request.user.username, request.POST['username'], count)
    user = Client.objects.get(user=User.objects.get(username=request.user.username))
    print(user)
    accounts = Account.objects.filter(client=user)
    print(accounts)
    context = {'user': user, 'accounts': accounts}
    return render(request, 'likePage.html', context)


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


def instaPost(user):
    try:
        print('insta login ', user)
        user = Client.objects.get(user=User.objects.get(username=user))

        for acc in Account.objects.filter(client=user):
            instaCli = InstagramClient(acc.username, acc.password)
            instaCli.upload(Post.objects.filter(client=user, status=True))
    except:
        pass


def instaFollow(user, someone,count):
    print('insta login ', user)

    user = Client.objects.get(user=User.objects.get(username=user))

    for acc in Account.objects.filter(client=user)[:count]:
        try:
            instaCli = InstagramClient(acc.username, acc.password)
            instaCli.followSomeOne(instaCli.get_user_id(someone))
        except:
            pass


def instaLike(user, targetMedia, count):
    print('count', count)


    user = Client.objects.get(user=User.objects.get(username=user))

    for acc in Account.objects.filter(client=user)[:count]:
        try:
            instaCli = InstagramClient(acc.username, acc.password)
            instaCli.api.like(instaCli.get_media_id(targetMedia))
        except:
            pass


def instaComment(user, media, text, count):
    print('insta login ', user)
    try:
        user = Client.objects.get(user=User.objects.get(username=user))

        for acc in Account.objects.filter(client=user)[:count]:
            instaCli = InstagramClient(acc.username, acc.password)
            instaCli.api.comment(instaCli.get_media_id(media), text)
    except:
        pass


def instaCreate(user, count):
    print('running bot for ', user, count)
    if count is None:
        count = 1
    runBot(user, count)
