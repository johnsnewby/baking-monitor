import requests

node = "http://tezos.newby.org:8732"
chain = "NetXjD3HPJJjmcd"

def preamble():
    return "%s/chains/%s" % (node, chain)

def req(url):
    print(url)
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

def missed_slots(block):
    slots = endorsers_slots(block["header"]["predecessor"])
    endorsements = list(filter(lambda x: x["contents"][0]["kind"] == "endorsement", block["operations"][0]))
    for endorsement in endorsements:
        delegate = endorsement["contents"][0]["metadata"]["delegate"]
        for slot in endorsement["contents"][0]["metadata"]["slots"]:
            assert slots[slot] == delegate
            slots[slot] = None
    return slots

def endorsements(block): # list of accounts which actually endorsed a block
    endorsements = list(filter(lambda x: x["contents"][0]["kind"] == "endorsement", block["operations"][0]))
    endorsers = list(map(lambda x: x["contents"][0]["metadata"]["delegate"], endorsements))
    return endorsers

def predecessor(hash): # predecessor block hash
    return hash["header"]["predecessor"]

def missed_endorsements_previous(hash):
    block1 = tz_block_by_hash(hash)
    block0 = predecessor(block1)
    potential_endorsers = endorsers(tz_endorsing_rights(block0))
    endorsed = endorsements(block1)
    return [item for item in potential_endorsers if item not in endorsed]

head = tz_head()
print(head)
print(missed_endorsements_previous(head))
missed = missed_slots(tz_block_by_hash(head))
for i in range(0, len(missed)):
    if missed[i] != None:
        print("%d: %s" % (i, missed[i]))

#print(endorsers(tz_endorsing_rights(tz_head())))

"""


# url tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks
# curl tezos.newby.org:8732/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy
# curl tezos.newby.org:8732/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy
# curl tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/
# curl tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/ | jq .
# curl tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/ | jq .|less
q# curl tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/baking_rights | jq .|less
# curl tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/baking_rights
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/baking_rights
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/helpers/baking_rights
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/helpers/baking_rights |jq .
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/helpers/baking_rights |jq .|less
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/helpers/endorsing_rights |jq .|less
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/BKvRtEQwjKuP1aneC5aLGPbNyLjXzfWkW2E2arrBFfULwDZcWPy/helpers/endorsing_rights?all=true |jq .|less
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/598443,/helpers/endorsing_rights?all=true |jq .|less
# curl  -v tezos.newby.org:8732/chains/NetXjD3HPJJjmcd/blocks/598443/helpers/endorsing_rights?all=true |jq .|less
# dmesg
# """
