# Enigma Template Code for CNU Information Security 2022
# Resources from https://www.cryptomuseum.com/crypto/enigma

# This Enigma code implements Enigma I, which is utilized by 
# Wehrmacht and Luftwaffe, Nazi Germany. 
# This version of Enigma does not contain wheel settings, skipped for
# adjusting difficulty of the assignment.

from copy import deepcopy
from ctypes import ArgumentError

# Enigma Components
ETW = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

# 회전한 수를 카운트하는 cnt와 wire와 maping 될 A~Z 문자열인 match
WHEELS = {
    "I" : {
        "wire": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
        "turn": 16,
        "cnt": 0,
        "match": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    },
    "II": {
        "wire": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
        "turn": 4,
        "cnt": 0,
        "match": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    },
    "III": {
        "wire": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
        "turn": 21,
        "cnt": 0,
        "match": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    }
}

UKW = {
    "A": "EJMZALYXVBWFCRQUONTSPIKHGD",
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL"
}

# Enigma Settings
SETTINGS = {
    "UKW": None,
    "WHEELS": [],
    "WHEEL_POS": [],
    "ETW": ETW,
    "PLUGBOARD": []
}

def apply_settings(ukw, wheel, wheel_pos, plugboard):
    if not ukw in UKW:
        raise ArgumentError(f"UKW {ukw} does not exist!")
    SETTINGS["UKW"] = UKW[ukw]

    wheels = wheel.split(' ')
    for wh in wheels:
        if not wh in WHEELS:
            raise ArgumentError(f"WHEEL {wh} does not exist!")
        SETTINGS["WHEELS"].append(WHEELS[wh])

    wheel_poses = wheel_pos.split(' ')
    for wp in wheel_poses:
        if not wp in ETW:
            raise ArgumentError(f"WHEEL position must be in A-Z!")
        SETTINGS["WHEEL_POS"].append(ord(wp) - ord('A'))
    
    plugboard_setup = plugboard.split(' ')
    for ps in plugboard_setup:
        if not len(ps) == 2 or not ps.isupper():
            raise ArgumentError(f"Each plugboard setting must be sized in 2 and caplitalized; {ps} is invalid")
        SETTINGS["PLUGBOARD"].append(ps)

# Enigma Logics Start

# Plugboard
def pass_plugboard(input):
    for plug in SETTINGS["PLUGBOARD"]:
        if str.startswith(plug, input):
            return plug[1]
        elif str.endswith(plug, input):
            return plug[0]

    return input

# ETW
def pass_etw(input):
    return SETTINGS["ETW"][ord(input) - ord('A')]

# Wheels
def pass_wheels(input, reverse = False):
    # Implement Wheel Logics
    # Keep in mind that reflected signals pass wheels in reverse order

    # 처음 wheel 통과
    if reverse == False:
        idx = ETW.find(input)
        i = SETTINGS["WHEELS"][0]["wire"][idx]
        # print(SETTINGS["WHEELS"][0]["wire"])
        # print(SETTINGS["WHEELS"][0]["match"])
        # print(i)

        idx = SETTINGS["WHEELS"][0]["match"].find(i)
        i = SETTINGS["WHEELS"][1]["wire"][idx]
        # print(idx)
        # print(SETTINGS["WHEELS"][1]["wire"])
        # print(SETTINGS["WHEELS"][1]["match"])
        # print(i)
        
        idx = SETTINGS["WHEELS"][1]["match"].find(i)
        i = SETTINGS["WHEELS"][2]["wire"][idx]
        # print(idx)
        # print(SETTINGS["WHEELS"][2]["wire"])
        # print(SETTINGS["WHEELS"][2]["match"])
        # print(i)

        idx = SETTINGS["WHEELS"][2]["match"].find(i)
        i = ETW[idx]

    # 두번째 wheel 통과
    elif reverse == True:
        
        idx = ETW.find(input)
        i = SETTINGS["WHEELS"][2]["match"][idx]
        idx = SETTINGS["WHEELS"][2]["wire"].find(i)
        # print(input)
        # print(i)
        # print(idx)

        i = SETTINGS["WHEELS"][1]["match"][idx]
        idx = SETTINGS["WHEELS"][1]["wire"].find(i)
        # print(i)
        # print(idx)

        i = SETTINGS["WHEELS"][0]["match"][idx]
        idx = SETTINGS["WHEELS"][0]["wire"].find(i)
        # print(i)
        # print(idx)

        i = ETW[idx]
        # print(i)

    return i

# UKW
def pass_ukw(input):
    return SETTINGS["UKW"][ord(input) - ord('A')]

# wheel 도는것을 카운트하고, 그에 따라서 wire와 match를 shift 한다.
def rotate_wheels():
    # Implement Wheel Rotation Logics
    
    # 첫번째 휠 / 왼쪽 shift / cnt 증가
    SETTINGS["WHEELS"][0]["wire"] = SETTINGS["WHEELS"][0]["wire"][1:] + SETTINGS["WHEELS"][0]["wire"][0]
    SETTINGS["WHEELS"][0]["match"] = SETTINGS["WHEELS"][0]["match"][1:] + SETTINGS["WHEELS"][0]["match"][0]
    SETTINGS["WHEELS"][0]["cnt"] += 1
    if SETTINGS["WHEELS"][0]["cnt"] == SETTINGS["WHEELS"][0]["turn"]:
        SETTINGS["WHEELS"][0]["cnt"] = 0
        SETTINGS["WHEELS"][1]["wire"] = SETTINGS["WHEELS"][1]["wire"][1:] + SETTINGS["WHEELS"][1]["wire"][0]
        SETTINGS["WHEELS"][1]["match"] = SETTINGS["WHEELS"][1]["match"][1:] + SETTINGS["WHEELS"][1]["match"][0]
        SETTINGS["WHEELS"][1]["cnt"] += 1

        if SETTINGS["WHEELS"][1]["cnt"] == SETTINGS["WHEELS"][1]["turn"]:
            SETTINGS["WHEELS"][1]["cnt"] = 0
            SETTINGS["WHEELS"][2]["wire"] = SETTINGS["WHEELS"][2]["wire"][1:] + SETTINGS["WHEELS"][2]["wire"][0]
            SETTINGS["WHEELS"][2]["match"] = SETTINGS["WHEELS"][2]["match"][1:] + SETTINGS["WHEELS"][2]["match"][0]
            SETTINGS["WHEELS"][2]["cnt"] += 1
    pass

# wheel position을 설정하는 함수
def set_pos_select():

    for idx in range(3):
        wheel_wire = SETTINGS["WHEELS"][idx]["wire"]
        set_match = SETTINGS["WHEELS"][idx]["match"]
        for _ in range(SETTINGS["WHEEL_POS"][idx]):
            wheel_wire = wheel_wire[1:] + wheel_wire[0]
            set_match = set_match[1:] + set_match[0]

        SETTINGS["WHEELS"][idx]["wire"] = wheel_wire
        SETTINGS["WHEELS"][idx]["match"] = set_match
    
    pass

# Enigma Exec Start
plaintext = input("Plaintext to Encode: ")
ukw_select = input("Set Reflector (A, B, C): ")
wheel_select = input("Set Wheel Sequence L->R (I, II, III): ")
wheel_pos_select = input("Set Wheel Position L->R (A~Z): ")
plugboard_setup = input("Plugboard Setup: ")

apply_settings(ukw_select, wheel_select, wheel_pos_select, plugboard_setup)
set_pos_select()
enc_ch = ''

for ch in plaintext:
    rotate_wheels()

    encoded_ch = ch

    encoded_ch = pass_plugboard(encoded_ch)
    encoded_ch = pass_etw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch)
    encoded_ch = pass_ukw(encoded_ch)
    encoded_ch = pass_wheels(encoded_ch, reverse = True)
    encoded_ch = pass_plugboard(encoded_ch)

    enc_ch += encoded_ch

print(enc_ch)