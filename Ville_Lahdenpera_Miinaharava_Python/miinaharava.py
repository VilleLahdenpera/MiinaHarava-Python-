import random
import time
from colorama import Fore, Back, Style
import haravasto as hv
import alkuvalikko as av
import tilastot as ti


tila = {
    "nakyva": None, #Näkyvä kenttä
    "piilossa": None, #Piilossa oleva täytetty kenttä
    "vapaat": 0 #Avaamattomien ruutujen määrä
}


napit = {
    hv.HIIRI_VASEN: "vasen",
    hv.HIIRI_KESKI: "keski",
    hv.HIIRI_OIKEA: "oikea"
} 

def kasittele_hiiri(x, y, nappi, muokkausnapit):
    """
    Tätä funktiota kutsutaan kun käyttäjä klikkaa sovellusikkunaa hiirellä.
    Antaa hiiren sijainnin(x, y koordinaateilla) sekä painetun napin(hiiren vasen-, oikea tai keskinäppäin).
    """
    x,s = divmod(x, 40)
    y,t = divmod(y, 40) 
    #Pelin kulku:            
    if tila["nakyva"][y][x] != tila["piilossa"][y][x] and nappi == hv.HIIRI_VASEN and tila["nakyva"][y][x] != "0": #Ruudun aukaisu(ilman tulvatäyttöä)
        tila["nakyva"][y][x] = tila["piilossa"][y][x]
        ti.aika["vuorot"] += 1
    if nappi == hv.HIIRI_OIKEA: #Merkkaus
        if tila["nakyva"][y][x] == " ":
            tila["nakyva"][y][x] = "f"
        elif tila["nakyva"][y][x] == "f":
            tila["nakyva"][y][x] = " "
    if tila["piilossa"][y][x] == "x" and nappi == hv.HIIRI_VASEN: #Miinaan osuminen(Häviö)
        tila["piilossa"] == tila["nakyva"]
        hv.lopeta()
        print("____________________" + "\n" + "\n" + Fore.RED + "ASTUIT MIINAAN! PELI OHI!"+ "\n")
        print(Style.RESET_ALL + "____________________")
        ti.aika["lopetus"] = time.time()
        ti.tallenna("Häviö", av.alkutiedot["miinat"], av.alkutiedot["leveys"], av.alkutiedot["korkeus"], ti.aika["vuorot"])
    if tila["piilossa"][y][x] == "0" and nappi == hv.HIIRI_VASEN: #Tulvatäyttö
        tulvataytto(tila["nakyva"], x, y, tila["piilossa"])
    tila["vapaat"] = 0  #Voitto tarkistus
    for j, ruudut in enumerate(tila["nakyva"]): 
        for i, ruudut in enumerate(ruudut):
            if tila["nakyva"][j][i] == tila["piilossa"][j][i]:
                pass
            else:
                tila["vapaat"] += 1          
    if tila["vapaat"] <= av.alkutiedot["miinat"]: #Voitto(Avaamattomien ruutujen määrä = miinojen määrä
        hv.lopeta()
        print("____________________"+ "\n" + "\n" + Fore.GREEN + "KAIKKI MIINAT HARAVOITU! ONNEKSI OLKOON!"+ "\n")
        print(Style.RESET_ALL + "____________________")
        ti.aika["lopetus"] = time.time()
        ti.tallenna("Voitto", av.alkutiedot["miinat"], av.alkutiedot["leveys"], av.alkutiedot["korkeus"], ti.aika["vuorot"])

def piirra_kentta():
    """
    Käsittelijäfunktio, joka piirtää kaksiulotteisena listana kuvatun miinakentän
    ruudut näkyviin peli-ikkunaan. Funktiota kutsutaan aina kun pelimoottori pyytää
    ruudun näkymän päivitystä.
    """
    hv.tyhjaa_ikkuna()
    hv.piirra_tausta()
    hv.aloita_ruutujen_piirto()
    for y, ruutu in enumerate(tila["nakyva"]):
        for x, ruutux in enumerate(ruutu):
            hv.lisaa_piirrettava_ruutu(tila["nakyva"][y][x], (x*40), (y*40))
    hv.piirra_ruudut()
    hv.piirra_tekstia("", 1, 1, vari=(0, 0, 0, 255), fontti="serif", koko=32)

def laske_miinat(x, y, lista):
    """
    Laskee valitun ruudun(x ja y koordinaattien mukaan annettu) ympärillä olevat miinat.
    """
    korkeus = len(lista) - 1
    leveys = len(lista[0]) - 1
    n = 0
    if x == 0:
        xalku = x
        xloppu = x + 1
    elif x == leveys:
        xloppu = x
        xalku = x - 1
    else:
        xalku = x - 1
        xloppu = x + 1
    
    if y == 0:
        yalku = y
        yloppu = y + 1
    elif y == korkeus:
        yalku = y -1
        yloppu = y
    else:
        yalku = y - 1
        yloppu = y + 1
    for x in range(xalku, xloppu + 1):
        for y in range(yalku, yloppu + 1):
            if lista[y][x] == "x":
                n +=1
    return n
    
def miinoita(kentta, jaljella, n):
    """
    Asettaa kentällä N kpl miinoja satunnaisiin paikkoihin.
    """
    for miinat in range(n):
        ruutu = random.choice(jaljella)
        jaljella.remove(ruutu)
        kentta[ruutu[1]][ruutu[0]] = "x"
        
        
def numeroi(piilossaKentta):
    """
    Numeroi ruudut sen mukaan kuinka monta miinaa on sen ympärillä(8 ruutua).
    """
    for y, ruudut in enumerate(piilossaKentta):
        for x, ruutu in enumerate(ruudut):
            numero = laske_miinat(x, y, piilossaKentta)
            if piilossaKentta[y][x] == "x":
                pass
            else:
                piilossaKentta[y][x] = ("{}").format(numero)
                

def tulvataytto(nakyva, alku_x, alku_y, piilo):
    """
    Avaa kentällä vierekkäin olevat tyhjien ruutujen alueet siten, että
    se aloitetaan annetusta x, y -pisteestä.
    """
    lista = [[alku_x, alku_y]]
    while lista:
        pari = lista.pop()
        nakyva[pari[1]][pari[0]] = "0"
        korkeus = len(nakyva) - 1
        leveys = len(nakyva[0]) - 1
        x = pari[0]
        y = pari[1]
        if x == 0:
            xalku = x
            xloppu = x + 1
        elif x == leveys:
            xloppu = x
            xalku = x - 1
        else:
            xalku = x - 1
            xloppu = x + 1     
        if y == 0:
            yalku = y
            yloppu = y + 1
        elif y == korkeus:
            yalku = y - 1
            yloppu = y
        else:
            yalku = y - 1
            yloppu = y + 1
        for x in range(xalku, xloppu + 1):
            for y in range(yalku, yloppu + 1):
                if nakyva[y][x] == nakyva[pari[1]][pari[0]]:
                    pass
                else:    
                    if piilo[y][x] == "0":
                        lista.append((x, y))
                    if piilo[y][x] == "1" or piilo[y][x] == "2" or piilo[y][x] == "3" or piilo[y][x] == "4" or piilo[y][x] == "5" or piilo[y][x] == "6" or piilo[y][x] == "7" or piilo[y][x] == "8":
                        nakyva[y][x] = piilo[y][x]
                  

def luo_kentta(leveys, korkeus):
    """
    Luo näkyvän(tyhjän) kentän, piilossa olevan täytettävän kentän ja 
    miinoitus funktioon tarvittavan jaljellä kentän.
    """
    kentta = []
    piilossaKentta = []
    for rivi in range(korkeus):
        piilossaKentta.append([])
        for sarake in range(leveys):
            piilossaKentta[-1].append("0")
    for rivi in range(korkeus):
        kentta.append([])
        for sarake in range(leveys):
            kentta[-1].append(" ")
            jaljella = []
    for x in range(leveys):
        for y in range(korkeus):
            jaljella.append((x, y))        
    return kentta, piilossaKentta, jaljella        
        

def main():
    hv.lataa_kuvat("spritet")
    hv.luo_ikkuna(av.alkutiedot["leveys"]*40, av.alkutiedot["korkeus"]*40)
    hv.aseta_piirto_kasittelija(piirra_kentta)
    hv.aseta_hiiri_kasittelija(kasittele_hiiri)
    print("Peli käynnissä...")
    hv.aloita()


if __name__ == "__main__":
    while av.valikko():
        tila["nakyva"], tila["piilossa"], jaljella = luo_kentta(av.alkutiedot["leveys"], av.alkutiedot["korkeus"]) #Luo kentät
        miinoita(tila["piilossa"], jaljella, av.alkutiedot["miinat"]) #Miinoittaa kentän
        numeroi(tila["piilossa"]) #Asettaa numerot kentälle
        ti.aika["aloitus"] = time.time() #Aloittaa keston laskun
        main()