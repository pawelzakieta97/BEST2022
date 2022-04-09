import requests
import threading

class RaspberryController:
    def __init__(self, url):
        self.url = url

    def drive(self, amount):
        requests.post(self.url+'/drive', params={'amount': amount})

    def drive(self, amount):
        requests.post(self.url+'/drive', params={'amount': amount})

