import requests
import threading


class RaspberryController:
    def __init__(self, url):
        self.url = url
        self.enable = True

    def drive(self, amount):
        if self.enable:
            resp = requests.post(self.url+'/drive', params={'power': amount})
            return resp.content

    def turn(self, amount):
        if self.enable:
            resp = requests.post(self.url+'/turn', params={'angle': amount})
            return resp.content


if __name__ == '__main__':
    rc = RaspberryController('http://raspberrypi.local:5000')
    #resp = rc.drive(1)
    # pass
    resp = rc.turn(-0.2)
