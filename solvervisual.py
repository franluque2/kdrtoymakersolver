# Small World Simulator

import requests
import json
import pprint
import time

# Step 1: YDK Extractor
with open('KDR 2 Inventory.ydk') as f:
    deck = f.read().splitlines()

deck.pop(0)
deck.pop(0)
decksize = deck.index("#extra")
extradeck = deck[decksize:]
extradeck.pop(0)
extradeck.pop()

extradeck = list(set(extradeck))
deck = deck[:decksize]
deck = list(set(deck))

deckmonsters = {}
extradeckmonsters = {}
final = {}
monsterbridges = {}

# Step 2: API Calls
for card in deck:
    #print(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    info = json.loads(response.text)
    #print(info)
    info = info["data"][0]
    print(info["name"]) 

    if "Monster" in info["type"]:
        deckmonsters[info["name"]] = {"ATK": info["atk"],"DEF": info["def"], "Attribute": info["attribute"],"Type": info["race"], "Level": info["level"]}

for card in extradeck:
    #print(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    info = json.loads(response.text)
    #print(info)
    info = info["data"][0]
    print(info["name"]) 
    if "Monster" in info["type"]:
        final[info["name"]] = {"ATK": [],"DEF": [], "Attribute": [],"Type": [], "Level": []}
    if info["type"]=="Link Monster":
        extradeckmonsters[info["name"]] = {"ATK": info["atk"],"DEF": -1, "Attribute": info["attribute"],"Type": info["race"], "Level": -1}
    if info["type"]=="XYZ Monster":
        extradeckmonsters[info["name"]] = {"ATK": info["atk"],"DEF": info["def"], "Attribute": info["attribute"],"Type": info["race"], "Level": -1}
    elif "Monster" in info["type"]:
        extradeckmonsters[info["name"]] = {"ATK": info["atk"],"DEF": info["def"], "Attribute": info["attribute"],"Type": info["race"], "Level": info["level"]}

deckmonsters.update(extradeckmonsters)


# Step 3: Actual Logic

def getScore(card,comparison):
    score = 0
    for key in card:
        if card[key] == comparison[key]:
            score = score + 1
            keyR = key
    if score == 1:
        return keyR
    else:
        return 'no'

for mdMon in deckmonsters:
    for edMon in extradeckmonsters:
        key = getScore(deckmonsters[mdMon], extradeckmonsters[edMon])
        if key != 'no':
            final[edMon][key].append(mdMon)

f = open("output.txt", "a")
f.truncate(0)
for card in final:
    string = ""
    string += card
    string += ":\n"
    for key in final[card]:
        string += key
        string += ":("
        string += "/".join(final[card][key])
        string += ")\n"
    string += "\n"
    f.write(string)