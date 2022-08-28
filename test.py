import random
import time
def random_letters(len = random.randint(3,9)):
    import random
    letters = ["a","b","c","d","e","f",'g',"h","i","j","k","l","m","n",'o','p','q','r','s','t','u','v','w','x','y','z']
    slovo = ''
    for i in range(len):
        slovo = slovo+letters[random.randint(0,25)]
    return slovo

def lidder(slovo):
    v = 1
    for i in slovo:
        for l in range(v):
            print(i,end = '')
        print()
        time.sleep(1)
        v+=1

def kol_vo(numb):
    kol = 0
    for i in str(numb):
        if int(i)%2==0:
            kol+=1
    return kol

lidder(random_letters())
print(kol_vo(random.randint(1,1000000)))