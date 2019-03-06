import time
import urllib.request
from random import randint

from InstagramAPI import InstagramAPI
import sys, json, os
import requests
from django.conf import settings


class InstagramClient(object):
    def __init__(self, username, password):
        # Attempt authentication
        try:
            if (self, username != None and password != None):
                self.username = username
                self.password = password
                self.api = InstagramAPI(username, password)
                self.api.login()
                print('Login was successful for {}'.format(self.username))
            else:
                return
        except:
            print(self, "Error: Authentication Failed")

    def getValueFromJson(self, json, value):
        try:
            return json[value]
        finally:
            return ""

    def likeMainFeed(self, user_id):
        self.getFeed(user_id)
        # print(self.api.LastJson)
        mediaFeed = self.api.LastJson['items']
        for post in mediaFeed:
            self.api.like(post['id'])
            print(post['user']['full_name'])

    def getSelfPost(self):
        return self.getPosts(self.api.username_id)

    def getPosts(self, user_id):
        list = []
        self.api.getSelfUserFeed()
        for post in self.api.LastJson['items']:
            try:

                id = post['id']
                if post['caption'] is not None:
                    caption = post['caption']['text']
                else:
                    caption = ""
                print(post)
                if post['image_versions2'] is not None:
                    image = post['image_versions2']['candidates'][0]['url']
                else:
                    image = ""
                list.append([id, caption, image])
            except:
                continue
        return list

    def changePP(self, loc):
        self.api.changeProfilePicture(loc)

    def getCommenters(self, postid):
        commenters = []
        self.api.getMediaComments(str(postid))
        for comments in self.api.LastJson['comments']:
            commenters.append(comments['user']['username'])
        # print(self.api.LastJson['comments']['user']['username'])
        return commenters

    def getHashtagPosts(self, hastagName):

        self.api.getHashtagFeed(hastagName)
        posts = []
        # print(self.api.LastJson)
        for items in self.api.LastJson['ranked_items']:
            posts.append(items)

        return posts

    def makePrivate(self, status=True):
        if status:
            self.api.setPrivateAccount()
            print('{} is private now'.format(self.username))
        else:
            self.api.setPublicAccount()
            print('{} is public now'.format(self.username))

    def directMessage(self, user_id, message):
        return

    def followSomeOne(self, user_id):
        self.api.follow(user_id)
        if self.api.LastJson['status'] == 'ok':
            print("{} Takip edilen hesap {}".format(self.username.upper(), user_id))
            return True
        else:
            return False

    def followSomeOneWithId(self, user_id):
        self.api.follow(str(user_id))
        if self.api.LastJson['status'] == 'ok':
            return True
        else:
            return False

    def getFollowers(self, user_id, maxid=1000):
        self.api.getUserFollowers(user_id)
        print(self.api.LastJson)
        return (self.api.LastJson['users'])

    def getFollowings(self, user_id, maxid=1000):
        self.api.getUserFollowings(user_id)
        return (self.api.LastJson['users'])

    def followSomePageFollowers(self, user_id):
        followers = self.getFollowers(user_id)
        for follower in followers:
            if self.followSomeOneWithId(follower['pk']):
                print("{} Sayfasından {} isimli hesap takip edildi".format(self.username, follower['username']))
            else:
                print("{} Sayfasından {} isimli hesap takip edilemedi".format(self.username, follower['username']))

    def getProfileInfo(self, user_id):
        self.api.getUsernameInfo(user_id)
        profilePicture = self.api.LastJson['user']['profile_pic_url']
        fullName = self.api.LastJson['user']['full_name']
        isPrivate = self.api.LastJson['user']['is_private']
        mediaCount = self.api.LastJson['user']['media_count']
        isPrivate = self.api.LastJson['user']['is_private']
        followerCount = self.api.LastJson['user']['follower_count']
        followingCount = self.api.LastJson['user']['following_count']
        biography = self.api.LastJson['user']['biography']
        return locals()

    def getRequests(self):
        self.api.getSelfUsernameInfo()
        # print(self.api.LastJson)

    def get_media_id(self, url):
        req = requests.get('https://api.instagram.com/oembed/?url={}'.format(url))
        media_id = req.json()['media_id']
        return media_id

    def upload(self, list):
        print(list)
        for l in list:
            print("Now Uploading this photo to instagram: " + l.text)

            # urllib.request.urlretrieve(l,
            #                            'temp.jpg')
            print(l.image.path)
            self.api.uploadPhoto(l.image.path, l.text)
            n = randint(5, 10)
            print("Sleep upload for seconds: " + str(0.1))
            l.status = False
            l.save()
            time.sleep(n)

    def deleteAllMedia(self):
        for media in self.getFeed(self.api.username_id):
            self.api.deleteMedia(media[0])
        return

    def unfollow(self, user_id):
        self.api.unfollow(user_id)
        if self.api.LastJson['status'] == 'ok':
            print("Takipden cikarilan hesap {}".format(user_id))
            return True
        else:
            return False

    def unfollowAll(self):
        followings = self.getFollowings(self.get_user_id(self.username))
        for user in followings:
            self.unfollow(user['pk'])

    def getFeed(self, user_id):
        list = []
        self.api.getUserFeed(usernameId=user_id)
        print(self.api.LastJson)

        for post in self.api.LastJson['items']:
            text = ""
            if 'caption' in post and post['caption'] is not None:
                if 'text' in post['caption']:
                    text = post['caption']['text']
            img = ""
            if ('image_versions2' in post):
                img = post['image_versions2']['candidates'][0]['url']

            list.append([post['id'], text, img])

        return list

    # def getHashtag(self, user_id):
    #     list = []
    #     self.api.getHashtagFeed(user_id)
    #     print(self.api.LastJson)
    #     from database import instertPic
    #     for post in self.api.LastJson['items']:
    #         try:
    #             text = ""
    #             if 'caption' in post and post['caption'] is not None:
    #                 if 'text' in post['caption']:
    #                     text = post['caption']['text']
    #             img = ""
    #             if ('image_versions2' in post):
    #                 img = post['image_versions2']['candidates'][0]['url']
    #
    #             list.append([post['id'], text, img])
    #             instertPic(img.strip(), text.strip(),user_id)
    #         except:
    #             continue
    #     return list

    def get_user_id(self, username):
        self.api.searchUsername(username)
        try:
            return self.api.LastJson["user"]["pk"]
        except Exception:
            print("username doesn't exist")
            return False

    def get_user_id_url(self, url):
        req = requests.get('https://api.instagram.com/oembed/?url={}'.format(url))
        media_id = req.json()['user_id']
        return media_id

    def register(self, username, password):
        return

# if __name__ == "__main__":
#     api = InstagramClient("furkankykc", "fur3808535qQ@")
#     # print(api.getFollowers())
#     # print (api.getProfileInfo("cubbelimehmedefendi"))
#
#     for i in (api.getPosts(api.api.username_id)):
#         print(i)
