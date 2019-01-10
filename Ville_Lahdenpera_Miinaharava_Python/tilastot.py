import time

aika = {
    "aika": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    "aloitus": None,
    "lopetus": None,
    "vuorot": 0
}

def tallenna(tulos, miinat, leveys, korkeus, vuorot):
    try:
        with open("tilastot.txt", "a") as kohde:
            kohde.write("{aika} Aika:{kesto:04}min {tulos} Vuorot:{vuorot} Kenttä:{leveys}x{korkeus} Miinat:{miinat}\n".format(aika=aika["aika"],
            kesto=round((aika["lopetus"] - aika["aloitus"]) / 60, 2),
            tulos=tulos,
            leveys=leveys,
            korkeus=korkeus,
            miinat=miinat,
            vuorot=vuorot))
            aika["vuorot"] = 0
    except IOError:
        print("Valittua tiedostoa ei voitu avata! Tilastoja ei voitu tallentaa.")
        
        
def avaa():
    try:
        with open("tilastot.txt") as lahde:
            for rivi in lahde.readlines():
                print(rivi)
            print("____________________")
    except IOError:
        print("Valittua tiedostoa ei voitu avata! Tilastoja ei voida tarkastella.")            