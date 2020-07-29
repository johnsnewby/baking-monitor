#!/usr/bin/env python

import requests

node = "http://tezos.newby.org:8732"
chain = "NetXjD3HPJJjmcd"

def preamble():
    return "%s/chains/%s" % (node, chain)

def req(url):
    resp = requests.get(url = url)
    return resp.json()

def tz_head():
    url = "%s/blocks" % (preamble())
    return req(url)[0][0]

def tz_block_by_hash(hash):
    url = "%s/blocks/%s" % (preamble(), hash)
    json = req(url)
    return json

def tz_endorsing_rights(hash): # endpoint to return list of endorsers
    url = "%s/blocks/%s/helpers/endorsing_rights" % (preamble(), hash)
    json = req(url)
    return json

def tz_baking_rights(hash): # endpoint to return list of bakers
    url = "%s/blocks/%s/helpers/baking_rights" % (preamble(), hash)
    json = req(url)
    return json

def endorsers(rights): # list of potential endorsers of a block
    endorsers = []
    for right in rights:
        endorsers.append(right["delegate"])
    return endorsers

def endorsers_slots(hash): # array of slots
    slots = [None] * 32
    rights = tz_endorsing_rights(hash)
    for right in rights:
        delegate = right["delegate"]
        for slot in right["slots"]:
            slots[slot] = delegate
    return slots

def baking_priorities(hash): # array of priorities
    priorities = [None] * 70 # ??
    json = tz_baking_rights(hash)
    for ele in json:
        priorities[ele["priority"]] = ele["delegate"]
    return priorities

# Take an array of slots, and clear out all the ones which received endorsements
def missed_slots(block):
    slots = endorsers_slots(block["header"]["predecessor"])
    endorsements = list(filter(lambda x: x["contents"][0]["kind"] == "endorsement", block["operations"][0]))
    for endorsement in endorsements:
        delegate = endorsement["contents"][0]["metadata"]["delegate"]
        for slot in endorsement["contents"][0]["metadata"]["slots"]:
            assert slots[slot] == delegate # be paranoid
            slots[slot] = None
    return slots

def endorsements(block): # list of accounts which actually endorsed a block
    endorsements = list(filter(lambda x: x["contents"][0]["kind"] == "endorsement", block["operations"][0]))
    endorsers = list(map(lambda x: x["contents"][0]["metadata"]["delegate"], endorsements))
    return endorsers

def predecessor(hash): # predecessor block hash
    return hash["header"]["predecessor"]

# How many of the endorsements planned in the previous block were missed?
def missed_endorsements_previous(block1):
    block0 = predecessor(block1)
    potential_endorsers = endorsers(tz_endorsing_rights(block0))
    endorsed = endorsements(block1)
    return [item for item in potential_endorsers if item not in endorsed]
