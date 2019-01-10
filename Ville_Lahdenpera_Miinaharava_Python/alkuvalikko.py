from colorama import Fore, Back, Style
import tilastot as ti

alkutiedot = {
    "leveys": None,
    "korkeus": None,
    "miinat": None
}

def valikko():
    while True:
        try:
            print("   " + Back.RED + "!MIINAHARAVA!" + Style.RESET_ALL + " ")
            valinta = int(input("   1: Aloita peli!" + "\n" + "   2: Tilastot" + "\n" + "   3: Lopeta"+ "\n" + "Anna toiminto(1-3):")) 
            if valinta == 3:
                return False
            elif valinta == 2:
                ti.avaa()
            elif valinta == 1:
                while True:
                    try:
                        leveys = int(input("Anna ruudukon leveys(5 - 20): "))
                        if not 5 <= leveys <= 20:
                           print("Anna arvo väliltä 5-20!")
                        else:
                            while True:
                                try:
                                    korkeus = int(input("Anna ruudukon korkeus(5 - 20): "))
                                    if not 5 <= korkeus <= 20:
                                        print("Anna arvo väliltä 5-20!")
                                    else:
                                        while True:
                                            try:
                                                miinat = int(input("Anna miinojen määrä(1 - {}): ".format((leveys*korkeus) - 2)))
                                                if not 1 <= miinat <= (leveys*korkeus) - 2:
                                                    print("Anna arvo väliltä 1-{}!".format((leveys*korkeus) - 2))
                                                else:
                                                    alkutiedot["leveys"] = leveys
                                                    alkutiedot["korkeus"] = korkeus
                                                    alkutiedot["miinat"] = miinat
                                                    return True
                                            except ValueError:
                                                print("Anna arvo väliltä 1-{}!".format((leveys*korkeus) - 2))        
                                except ValueError:
                                    print("Anna arvo väliltä 5-20!")                
                    except ValueError:
                        print("Anna arvo väliltä 5-20!")
            else:
                print("Anna arvo väliltä 1-3!")
        except ValueError:
            print("Anna arvo väliltä 1-3!")

            
