#!/usr/bin/env python

import sys
from monitor import *
import requests
import time

# Functions to notify missed endorsements and baking. Invoke using code similar to the below:
#
#
# my_bakers = [ "tz1bg47NeJ5wePnPds9XxCAeftYPwb94WcA8",
#               "tz1hf83sreSbzof7WakXiNbjizWVHwDyHFJi",
#               "tz1gtQpCsD4m65uyrwQeHanxUdt2c2k8jzcJ" ]
# def sms(msg):
#     data = {
#         "text": msg,
#         "key": PUT_KEY_HERE,
#         "from": "TezosMonitor",
#         "to": "0049123412345",
#     }
#     r = requests.post("https://www.smsprovider.examples.com/send", data = data)
#
# loop(my_bakers, sms)


def check(block, my_bakers, sms):
    missed = missed_slots(block)

    my_misses = []

    bake_priorities = baking_priorities(block["header"]["predecessor"])
    if bake_priorities[0] != block["metadata"]["baker"]:
        if bake_priorities[0] in my_bakers:
            my_misses.append("baker %s missed slot" % (bake_priorities[0]))

    for i in range(0, len(missed)):
        if missed[i] in my_bakers:
             my_misses.append("%d: %s" % (block["header"]["level"], missed[i]))

    if len(my_misses) > 0:
        msg = '|'.join(my_misses)
        sms(msg)

def loop(my_bakers, sms):
    last_level = 0
    while True:
        head = tz_head()
        block = tz_block_by_hash(head)
        level = block["header"]["level"]
        if last_level < level:
            last_level = level
            check(block, my_bakers, sms)
            print("Checked block at level %d" % (level))
        time.sleep(30)
