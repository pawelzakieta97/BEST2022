import datetime

import requests
import threading


class RaspberryController:
    def __init__(self, url):
        self.url = url
        self.enable = True

    def drive(self, amount):
        if self.enable:
            start = datetime.datetime.now()
            #resp = requests.post(self.url+'/drive', params={'power': amount})
            print(f'req_time: {datetime.datetime.now()-start}')

            return None #resp.content

    def turn(self, amount):
        if self.enable:
            start = datetime.datetime.now()
            resp = requests.post(self.url+'/turn', params={'angle': amount})
            print(f'req_time: {datetime.datetime.now()-start}')
            return resp.content


if __name__ == '__main__':
    rc = RaspberryController('http://raspberrypi.local:5000')
    #resp = rc.drive(1)
    # pass
    resp = rc.turn(-0.2)
