""" author: feezyhendrix

    this module contains followers generation
 """

import random
import string
from .config import Config


# generating name functions
boyNames = ["dalmatianscoreboard",
            "custardscoreboard",
            "adshooch",
            "scoreboardunknown",
            "bossyscoreboard",
            "smoothscoreboard",
            "drippingscoreboard",
            "scoreboardinternal",
            "pennyscoreboard",
            "shufflingscoreboard",
            "adsguerrilla",
            "eyeads",
            "progradescoreboard",
            "guitarads",
            "adswiddendream",
            "christiescoreboard",
            "adspredefine",
            "quesadillascoreboard",
            "adsalkyne",
            "adsimage",
            "scoreboardflagstick",
            "guilelessscoreboard",
            "sugarscoreboard",
            "adswithey",
            "themescoreboard",
            "sidneyscoreboard",
            "adsrebuttal",
            "mizzenscoreboard",
            "sabinoads",
            "adsharsh",
            "replayads",
            "adstrinity",
            "adsrejoice",
            "enderscoreboard",
            "mushilyads",
            "worldcupads",
            "adslucie",
            "uswayscoreboard",
            "adssculpture",
            "scoreboardpruit",
            "adsplace",
            "pupkerscoreboard",
            "defensiveads",
            "adssleuth",
            "adsinverianvie",
            "foilads",
            "caucasianscoreboard",
            "scoreboardsparkle",
            "scoreboardlizard",
            "scoreboardaccustom",
            "scoreboardalderman",
            "fridayscoreboard",
            "iconscoreboard",
            "whereasscoreboard",
            "adsbanjo",
            "bruntonscoreboard",
            "adssweetcorn",
            "aviatorscoreboard",
            "scoreboardjudgment",
            "scoreboardgender",
            "propertyscoreboard",
            "adsaqueduct",
            "cornishscoreboard",
            "adshaircut",
            "tommyads"]
def genName():

    girlNames = ["Alice", "Hana", "Clare", "Janet", "Daisy"]
    return ''.join(random.choice(boyNames) + ' ' + random.choice(girlNames))


# generating a username
def username(size=1, chars=string.ascii_lowercase + random.choice(['V', '_'])):
    return ''.join(random.choice(boyNames)).join(random.choice(chars) for _ in range(size))


# ge
def generatePassword():
    password = str(Config["password"])
    return password


def genEmail():
    return ''.join(username(12) + '@mail.com')
