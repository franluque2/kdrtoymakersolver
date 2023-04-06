# Small World Simulator

import requests
import json
import pprint
import time

# Step 1: YDK Extractor
with open('deck2.ydk') as f:
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
    time.sleep(0.3)

for card in extradeck:
    #print(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    response = requests.get(f"https://db.ygoprodeck.com/api/v7/cardinfo.php?id={card}")
    info = json.loads(response.text)
    #print(info)
    info = info["data"][0]
    print(info["name"]) 

    if "Monster" in info["type"]:
        extradeckmonsters[info["name"]] = {"ATK": info["atk"],"DEF": info["def"], "Attribute": info["attribute"],"Type": info["race"], "Level": info["level"]}
    time.sleep(0.3)

pprint.pprint(deckmonsters)
pprint.pprint(extradeckmonsters)


# Step 3: Actual Logic

def getScore(card,comparison, thirdcard):
    score = 0
    for key in card:
        if card[key] == thirdcard[key] and not (card[key] == comparison[key]):
            for key2 in card:
                if key!=key2 and comparison[key2] == thirdcard[key2] and not (card[key2] == comparison[key2]):
                    print(card[key])
                    score = score + 1
    return score


for card in deckmonsters:
    monsterbridges[card] = {}
    for key in deckmonsters:
        for third in extradeckmonsters:
            score = getScore(deckmonsters[card],deckmonsters[key],extradeckmonsters[third])
            if score == 1:
                print(f"Card {card} fuses with {key} into {third}")
                if not key in monsterbridges[card]:
                    monsterbridges[card][key]=[]
                monsterbridges[card][key].append(third)

                print(monsterbridges[card])
            

pprint.pprint(monsterbridges)

f = open("output.txt", "a")
f.truncate(0)
for card in monsterbridges:
    for key in monsterbridges[card]:
        for target in monsterbridges[card][key]:
            print(f"Fuse {card} + {key} ---> into {target}")
            f.write(f"Fuse {card} + {key} ---> into {target}\n" )