#!/usr/bin/env python

from notify import *

my_bakers = [ "tz1bg47NeJ5wePnPds9XxCAeftYPwb94WcA8",
              "tz1hf83sreSbzof7WakXiNbjizWVHwDyHFJi",
              "tz1gtQpCsD4m65uyrwQeHanxUdt2c2k8jzcJ" ]
def sms(msg):
    data = {
        "text": msg,
        "key": "SECRET",
        "from": "TezosMonitor",
        "to": "00491749352940",
    }
    r = requests.post("https://www.smsflatrate.net/schnittstelle.php", data = data)


loop(my_bakers, sms)
