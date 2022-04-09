import requests
import threading


class RaspberryController:
    def __init__(self, url):
        self.url = url

    def drive(self, amount):
        resp = requests.post(self.url+'/drive', params={'power': amount})
        return resp.content

    def turn(self, amount):
        resp = requests.post(self.url+'/turn', params={'angle': amount})
        return resp.content

if __name__ == '__main__':
    rc = RaspberryController('http://raspberrypi.local:5000')
    resp = rc.drive(1)
    # pass
    # resp = rc.turn(-1)
