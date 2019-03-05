import requests

from register.models import Proxy, Account, Client
from .config import Config
from .generateaccountinformation import genName, username, genEmail
import json
import re
from .instaRegister import create

from urllib.request import Request, urlopen
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import random


# custom class for creating accounts


class CreateAccount:
    def __init__(self, user, email, username, password, name, numberofaccounts):
        self.sockets = []
        self.email = email
        self.username = username
        self.password = password
        self.name = name
        self.numberofaccounts = numberofaccounts
        self.user = user
        self.url = "https://www.instagram.com/accounts/web_create_ajax/"
        self.headers = {
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
        self.proxyproc()
        self.__collect_sockets()

    def proxyproc(self):
        # proxies_req = Request('https://www.sslproxies.org/')
        # ua = UserAgent()
        # proxies_req.add_header('User-Agent',ua.random)
        # proxies_doc = urlopen(proxies_req).read().decode('utf8')
        # soup = BeautifulSoup(proxies_doc, 'html.parser')
        # proxies_table = soup.find(id='proxylisttable')
        #
        # # Save proxies in the array
        # for row in proxies_table.tbody.find_all('tr'):
        #     self.sockets.append(
        #         row.find_all('td')[0].string+":"+
        #         row.find_all('td')[1].string
        #     )
        # with open('Assets/proxies.txt') as fp:
        #     line = fp.readlines()
        #     for proxy in line:
        #         self.sockets.append(proxy.strip())
        for ip in Proxy.objects.all():
            self.sockets.append(ip.ip)

    # a private function to fetch custom proxies
    def __collect_sockets(self):
        r = requests.get("https://www.sslproxies.org/")
        matches = re.findall(r"<td>\d+.\d+.\d+.\d+</td><td>\d+</td>", r.text)
        revised_list = [m1.replace("<td>", "") for m1 in matches]
        for socket_str in revised_list:
            self.sockets.append(socket_str[:-5].replace("</td>", ":"))

    # account creation function
    def createaccount(self):
        payload = {
            'email': self.email,
            'password': self.password,
            'username': self.username,
            'first_name': self.name,
            'client_id': 'W6mHTAAEAAHsVu2N0wGEChTQpTfn',
            'seamless_login_enabled': '1',
            'gdpr_s': '%5B0%2C2%2C0%2Cnull%5D',
            'tos_version': 'eu',
            'opt_into_one_tap': 'false'
        }
        if len(self.sockets) > 0:
            current_socket = self.sockets.pop(0)
            # current_socket= '1.20.97.95:60867'
            proxies = {"http": "http://" + current_socket, "https": "https://" + current_socket}
            # proxies={'http': 'http://jmtosmmw-3j4wdl2dr7a1b@142.44.223.144:80'}
            try:
                request = requests.post(self.url, data=payload, proxies=proxies, headers=self.headers)
                response = json.loads(request.text)
                print(response)
                try:
                    if (response["account_created"] is False):
                        if (response["errors"]["password"]):
                            print(self.username, ':', self.email)

                            print(response["errors"]["password"]["message"])
                            quit()
                        elif (response["errors"]["ip"]):
                            print(self.username,':',self.email)
                            print(response["errors"]["ip"]["message"])
                        else:
                            pass
                        self.createaccount()
                    else:
                        acc = Account(username=self.username, password=self.password,
                                      client=Client.objects.get(username=self.user))
                        acc.save()
                        pass
                except:
                    pass
            except:
                print('Error!, Trying another Proxy {}'.format(current_socket))
                try:
                    Proxy.delete(Proxy.objects.filter(ip=current_socket))
                except(Exception):
                    pass
                self.createaccount()


def runBot(user, count=1):
    if count is None:
        count = 1
    for i in range(int(count)):
        account = CreateAccount(user, genEmail(), username(), str(Config['password']), genName(), count)
        account.createaccount()
    # create(username(), genName(), genEmail(),  str(Config['password']))
