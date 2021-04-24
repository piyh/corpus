import random
import logging

player1 = "warlock"
player2 = "oddWarrior"
turnDk1 = 10
turnDk2 = 15

def recursiveSum(x):
    assert isinstance(x,int)
    if x <= 0:
        return x
    rSum = recursiveSum(x-1) + x
    return rSum

def randOccur(value,percent):
    if random.random() <= percent:
        return True
    else:
        return False

def damage(damaged, amount):
    armor = damaged["armor"] - amount
    if armor < 0:
        damaged["hp"] = damaged["hp"] + armor#max(0,)
        armor = max(0,armor)
    damaged["armor"] = armor        

def hpAddArmor(fortitude):
    return fortitude["armor"] + fortitude["hp"]

def calculateGame(heroes,turnsAnalyzed, turnFatigueBegins):#,playerIsOdd, enemyIsOdd
    fatigue = 0
    for turn in range(1,turnsAnalyzed):
        if turn >= turnFatigueBegins:
                fatigue += 1   
        for count,hero in enumerate(heroes):
            damage(hero,fatigue)
            if randOccur(hero["bpDamage"],hero["bpUse%"]): 
                if turn < hero["turnDk"]:
                    hero["hp"] = min(30,hero["hp"]+hero["bpHeal"])
                    hero["armor"] += hero["bpArmor"]
                    damage(heroes[not count],hero["bpDamage"])
                elif turn == hero["turnDk"]:
                    hero["armor"] += 5
                else:
                    hero["hp"] = min(30,hero["hp"]+hero["dkHeal"])
                    hero["armor"] += hero["dkArmor"]
                    damage(heroes[not count],hero["dkDamage"])
                        

        print("{}\t{}\t{}\t{}\t{}\t{}\t{}".format(turn,heroes[0]["hp"],hpAddArmor(heroes[0]),heroes[1]["hp"],hpAddArmor(heroes[1]),fatigue,recursiveSum(fatigue)))


classes = { #bp for base hero power, dk for death knight hero power
	"druid":{ "class":"Druid", "bpDamage":1, "bpArmor":1,"bpHeal":0, "bpUse%":.4, "dkDamage":0,"dkArmor":3,"dkHeal":0,"dkuse%":.8},
	"oddWarrior":{ "class":"OddWarrior", "bpDamage":0, "bpArmor":4,"bpHeal":0, "bpUse%":.4, "dkDamage":0,"dkArmor":4,"dkHeal":0,"dkuse%":.8},
        "hunter":{ "class":"Hunter", "bpDamage":2, "bpArmor":0,"bpHeal":0, "bpUse%":.2, "dkDamage":0,"dkArmor":0,"dkHeal":0,"dkuse%":0},
	"mage":{ "class":"Mage", "bpDamage":1, "bpArmor":0,"bpHeal":0, "bpUse%":.1, "dkDamage":1,"dkArmor":0,"dkHeal":0,"dkuse%":.2},
	"priest":{ "class":"Priest", "bpDamage":0, "bpArmor":0,"bpHeal":2, "bpUse%":.1, "dkDamage":4,"dkArmor":0,"dkHeal":0,"dkuse%":.6},
	"rogue":{ "class":"Rogue", "bpDamage":1, "bpArmor":0,"bpHeal":0, "bpUse%":.6, "dkDamage":0,"dkArmor":0,"dkHeal":0,"dkuse%":0},
       	"oddRogue":{ "class":"OddRogue", "bpDamage":2, "bpArmor":0,"bpHeal":0, "bpUse%":.7, "dkDamage":2,"dkArmor":0,"dkHeal":0,"dkuse%":.9},
	"warlock":{ "class":"Warlock", "bpDamage":0, "bpArmor":0,"bpHeal":-2, "bpUse%":.4, "dkDamage":3,"dkArmor":0,"dkHeal":3,"dkuse%":.8}
	}

player = {**classes[player1],"hp":30,"armor":0,"turnDk":turnDk1}
enemy = {**classes[player2],"hp":30,"armor":0,"turnDk":turnDk2}
heroes = (player,enemy)

turnsAnalyzed = 45
turnFatigueBegins = 27

print("Turns\t{0} HP\t{0} with Armor\t{1} HP\t{1} with Armor\tFatigue for\tCumulative Fatigue".format(player["class"],enemy["class"]))
calculateGame(heroes,turnsAnalyzed, turnFatigueBegins)

