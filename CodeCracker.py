import random
import string 
from timeit import default_timer as timer

# reference: https://codepen.io/AfroDev/pen/emezKV
# 8-digits code with characters 
# Code Generator functions is for performance test

characters = string.ascii_uppercase + string.ascii_lowercase + string.digits


code = ''

def CodeGen(chars = characters):
    gencode = ''
    for _ in range(4):
        gen = ''.join(random.choice(chars) for _ in range(4))
        gencode += gen
    return gencode

def spliter(target):
    if len(target) <= 16 and len(target) > 8:
        if 16 - len(target) > 0:
            target = f'{target:0<16}'
            print(target)
        sp1 = target[:4]
        sp2 = target[4:8]
        sp3 = target[8:12]
        sp4 = target[12:16]

    elif len(target) == 8:
        sp1 = target[:4]
        sp2 = target[4:8]
        sp3 = '0000'
        sp4 = '0000'
    
    return sp1, sp2, sp3, sp4

def Cracker4(part):
    cracked = False
    a = ''
    b = ''
    c = ''
    d = ''

    while (cracked == False):
        for itemd in characters:
            d = itemd
            for itemc in characters:
                c = itemc
                for itemb in characters:
                    b = itemb
                    for itema in characters:
                        a = itema
                        if part == str(d) + str(c) + str(b) + str(a):
                            cracked = True
                            res = str(d) + str(c) + str(b) + str(a)
                            return res, cracked
                        else:
                            print(d, c, b, a)
                            
def Cracker8(target):
    tg1, tg2, tg3, tg4 = spliter(target)
    cracked = False
    start = timer()
    while cracked == False:
        code1, crkd1 = Cracker4(tg1)
        code2, crkd2 = Cracker4(tg2)
        if crkd1 == True and crkd2 == True:
            cracked = True
            end = timer()
            crkcode = code1 + code2
            print("successed. Cracking time: ", end - start)
            return crkcode
        else:
            print("Failed to Crack. ")
            exit 

def Cracker16(target):
    cracked = False
    tg1, tg2, tg3, tg4 = spliter(target)
    start = timer()
    while cracked == False:
        code1, crkd1 = Cracker4(tg1)
        code2, crkd2 = Cracker4(tg2)
        code3, crkd3 = Cracker4(tg3)
        code4, crkd4 = Cracker4(tg4)
        if crkd1 == True and crkd2 == True and crkd3 == True and crkd4 == True:
            cracked = True
            end = timer()
            crkcode = code1 + code2 + code3 + code4
            print("SuCCEsseD. ", end - start)
            return crkcode
        else:
            print("Failed to Crack. ")
            exit

def main():
    choice = input("Manual input - 1, RandomGen - 2 ")
    if choice == '1':
        code = input("The answer is? ")
    elif choice == '2':
        code = CodeGen()
    else:
        print("Wrong choice. exit")
        exit
    
    if len(code) > 8 and len(code) <= 16:
        print(len(code))
        crked = Cracker16(code)
        print("Answer: ", code, "Cracked:", crked)

    elif len(code) <= 8:
        crked=Cracker8(code)
        print("Answer: ", code, "Cracked:", crked)


if __name__ == "__main__":
    main()
