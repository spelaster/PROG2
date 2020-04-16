import csv
import json
import re
import orodja
import matplotlib.pyplot as plt
import string


def zapisi_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari csv datoteko'''
    orodja.pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


def zapisi_json(objekt, ime_datoteke):
    '''Iz danega objekta ustvari json datoteko'''
    orodja.pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)


vzorec = re.compile(
    # naslov
    r'aria-level=\'4\'>(?P<naslov>[^<|(]*[^ |(|<]).*?'
    # avtor
    r'<span itemprop="name">(?P<avtor>.*?)</span>.*?'
    # povprečna ocena
    r' (?P<ocena>\d{1}\.\d{2}) avg rating.*?'
    # ocena na podlagi števila glasovalcev in njihovih ocen
    # r'(?P<score>.*?).*?'
    r'score: (?P<score>.*?)</a>.*?'
    # stevilo glasovalcev
    r'>(?P<glasovalci>[\d|,]*) people voted.*?',
    re.DOTALL
)


def cisti_podatki(podatki):
    podatki_knjige = podatki.groupdict()
    podatki_knjige['ocena'] = float(podatki_knjige['ocena'].replace(',', '.'))
    podatki_knjige['naslov'] = str(podatki_knjige['naslov'].replace('&quot;', '"'))
    podatki_knjige['score'] = float(podatki_knjige['score'].replace(',', '.'))
    podatki_knjige['glasovalci'] = int(podatki_knjige['glasovalci'].replace(',', ''))
    return podatki_knjige


for i in range(1, 11):
    url = ('https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page={}').format(i)
    orodja.shrani_spletno_stran(url, 'stran-{}.html'.format(i))

podatki = []
for stran in range(1, 11):
    vsebina = orodja.vsebina_datoteke('stran-{}.html'.format(stran))
    for ujemanje in vzorec.finditer(vsebina):
        podatki_knjige = cisti_podatki(ujemanje)
        podatki.append(podatki_knjige)
zapisi_csv(podatki, ['naslov', 'avtor', 'ocena', 'score', 'glasovalci'], 'knjige21.csv')
zapisi_json(podatki, 'knjige.json')


def vrstice_naslovi_avtorji(dat):
    '''
    Vrne koliko knjig imamo med podatki.
    '''
    stevec = 0
    with open(dat, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for vrstica in csv_reader:

            if stevec == 0:
                print('Imena stolpcev so ' + str(vrstica))
                pass
            if len(vrstica) == 0:
                if stevec == 0:
                    stevec = 1
            else:
                #naslov = vrstica[0]
                #avtor = vrstica[1]
                #ocena = vrstica[2]
                #score = vrstica[3]
                #glasovalci = vrstica[4]
                print('naslov: ' + vrstica[0] + 'avtor: ' + vrstica[1] + '.')
                stevec += 1
        print('Nasa datoteka ima ' + str(stevec - 1) + ' vrstic s podatki o knjigah.')


def avtor_knjige(avtor):
    '''
    Za izbranega avtorja pove, koliko njegovih del je v datoteki s podatki.
    '''
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        koliko = 0
        naslovi = []
        for vrstica in csv_reader:
            if len(vrstica) == 0:
                pass
            else:
                if vrstica[1] == avtor:  # če je avtor dela enak avtorju trenutne vrstice
                    naslovi.append(vrstica[0])  # dodamo naslov knjige k naslovom njegovih del
                    koliko += 1
        nas = ', '.join(naslovi)
        kdo = str(avtor)
        if koliko == 0:
            print('Avtor/ica ' + kdo + ' ni napisal/a nobenega dela, ki je v datoteki "knjige21.csv"\.')
        elif koliko == 1:
            print('Avtor/ica ' + kdo + ' je napisal/a eno delo z naslovom ' + nas + ', ki je v datoteki "knjige21.csv".')
        elif koliko == 2:
            print('Avtor/ica ' + kdo + ' je napisal/a dve deli z naslovoma ' + nas + ', ki sta v datoteki "knjige21.csv".')
        elif koliko == 3:
            print('Avtor/ica ' + kdo + ' je napisal/a tri dela z naslovi ' + nas + ', ki so v datoteki "knjige21.csv".')
        elif koliko == 4:
            print('Avtor/ica ' + kdo + ' je napisal/a štiri dela z naslovi ' + nas + ', ki so v datoteki "knjige21.csv".')
        else:
            print('Avtor/ica ' + kdo + ' je napisal/a ' + str(koliko) + ' del z naslovi: ' + nas + ', ki so v datoteki "knjige21.csv"')

        '''
            >>> avtor_knjige(J.K. Rowling)
            Avtor/ica J.K. Rowling je napisal/a 5 del z naslovi: Harry Potter and the Deathly Hallows,
            Harry Potter and the Half-Blood Prince, Harry Potter and the Order of the Phoenix,
            The Tales of Beedle the Bard, The Casual Vacancy.
            >>> avtor_knjige(Enid Bliton)
            Avtor/ica Enid Bliton ni napisal/a nobenega dela.
            >>> avtor_knjige(Markus Zusak)
            Avtor/ica Markus Zusak je napisal/a dve deli z naslovoma The Book Thief, I Am the Messenger, ki sta v datoteki "knjige21.csv".
        '''


def min_ocena(ocena):
    '''
    Funkcija izpiše naslove, avtorje ter oceno knjig, ki imajo oceno enako ali višjo vnešeni oceni.
    '''
    stevec = 0
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        knjige = []
        for vrstica in csv_reader:
            if stevec == 0:  # prve vrstice z imeni stolpcev ne štejemo
                pass
            elif len(vrstica) == 0:  # preskočimo prazne vrstice
                pass
            else:
                if float(vrstica[2]) >= float(ocena):  # če je ocena višja ali enaka željeni oceni
                    knjige.append((vrstica[0], vrstica[1], vrstica[2]))  # dodamo naslov, avtorja in oceno v seznam
            stevec += 1
        print('Knjige z oceno, višjo ali enako ' + str(ocena) + ', so: ' + str(knjige) + '.')

    '''
        >>> min_ocena(5)
        Knjige z oceno, višjo ali enako 5.0, so: [("I'm Unapologetically Single And More Than OK With It", 
        'Justin Ho', '5.0'), ('Goals, Obstacles And Gratitude', 'Justin Ho', '5.0'), ('10% Everything', 'Justin Ho', '5.0'), 
        ('Self-Improvement And Success', 'Justin Ho', '5.0'), ('Life Amplifiers Daily Devotional', 'Justin Ho', '5.0'), 
        ('Dream Big, Live Bigger', 'Justin Ho', '5.0'), ('Self-Esteem - Self = Esteem', 'Justin Ho', '5.0'), 
        ('The Old Has Gone, The New Is Here', 'Justin Ho', '5.0'), ('How To Develop A Million Dollar Mindset', 'Justin Ho', '5.0'), 
        ('Stop Auto-Piloting', 'Justin Ho', '5.0'), ('Your Skill, Your Wealth Builder', 'Justin Ho', '5.0'), 
        ('The Caves: Book One - The Event', 'Melody Laughlin', '5.0'), ('The Creation of Me, Them and Us', 'Heather  Marsh', '5.0'), 
        ('Moonlit Tours', 'Alistair McHarg', '5.0'), ("Lady Thatcher's Wink", 'David Arscott', '5.0'), 
        ('Telling Time by the Shadows', 'John     Fitzgerald', '5.0'), ('The Brutus Gate: A Bailey Crane Mystery', 'Billy Ray Chitwood', '5.0')].
        '''


# če upoštevamo še glasove, dobimo malo drugačno sliko:
def min_ocena_glasovi(ocena, glasovi):
    ''' Funkcija izpiše naslove, avtorje, oceno in število glasov knjig,
        ki imajo oceno enako ali višjo vnešeni oceni in zadostno število glasov. '''
    stevec = 0
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        knjige = []
        for vrstica in csv_reader:
            if stevec == 0:  # prve vrstice z imeni stolpcev ne štejemo
                pass
            elif len(vrstica) == 0:  # preskočimo prazne vrstice
                pass
            else:
                if (float(vrstica[2]) >= float(ocena)) and (float(vrstica[4]) >= float(glasovi)):
                    # če je ocena višja ali enaka željeni oceni in je število glasov zadostno
                    knjige.append((vrstica[0], vrstica[1], vrstica[2],
                                   vrstica[4]))  # dodamo naslov, avtorja, oceno in glasove v seznam
            stevec += 1
        print('Knjige z oceno, višjo ali enako ' + str(ocena) + ', in z vsaj ' + str(glasovi) + ' glasovi so: ' + str(knjige) + '.')

        '''
        >>> min_ocena_glasovi(4.6, 100)
        Knjige z oceno, višjo ali enako 4.6, in z vsaj 100 glasovi so: [('Harry Potter and the Deathly Hallows', 'J.K. Rowling', '4.62', '3995'), 
        ('Una Historia de Ayer', 'Sergio Cobo', '4.65', '119')]
        '''


def stevilo_z_oceno(ocena_spodaj, ocena_zgoraj):
    ''' vrne število knjig, ki se nahajajo med določenima ocenama - od spodnje do vključno zgornje). '''
    stevec = 0
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        koliko = 0
        knjige = []
        for vrstica in csv_reader:
            if stevec == 0:  # prve vrstice z imeni stolpcev ne štejemo
                pass
            elif len(vrstica) == 0:  # preskočimo prazne vrstice
                pass
            else:
                if (float(vrstica[2]) > float(ocena_spodaj)) and (float(vrstica[2]) <= float(ocena_zgoraj)):
                    # če je ocena višja od ocena_spodaj in nižja ali enaka ocena_zgoraj
                    # knjige.append((vrstica[0], vrstica[1], vrstica[2])) # dodamo naslov, avtorja in oceno v seznam
                    koliko += 1
            stevec += 1
        print('Knjig z oceno med ' + str(ocena_spodaj) + ' in ' + str(ocena_zgoraj) + ' je ' + str(koliko) + '.')

        '''
        >>> stevilo_z_oceno(4, 4.6)
        Knjig z oceno med 4 in 4.6 je 1002.
        '''


def razpored_knjig_po_oceni(razmik):
    ''' Vrne koliko knjig se nahaja med določenima ocenama, ocene so razporejene po danem razmaku.
        Upoštevamo, da je najvišja ocena enaka 5. '''
    i = 0
    sez = []
    while i + razmik <= 5:
        j = i + razmik
        sez.append(stevilo_z_oceno(i, j))
        i += razmik
    '''
    >>> razpored_knjig_po_oceni(0.5)
        Knjig z oceno med 0 in 0.5 je 0.
        Knjig z oceno med 0.5 in 1.0 je 0.
        Knjig z oceno med 1.0 in 1.5 je 0.
        Knjig z oceno med 1.5 in 2.0 je 0.
        Knjig z oceno med 2.0 in 2.5 je 0.
        Knjig z oceno med 2.5 in 3.0 je 5.
        Knjig z oceno med 3.0 in 3.5 je 77.
        Knjig z oceno med 3.5 in 4.0 je 848.
        Knjig z oceno med 4.0 in 4.5 je 963.
        Knjig z oceno med 4.5 in 5.0 je 105.
    '''


def razpored_knjig_ocena(razmik):
    ''' Vrne koliko knjig se nahaja med določenima ocenama, ocene so razporejene po danem razmaku.
        Upoštevamo, da je najnižja ocena enaka 3 in najvišja ocena enaka 5.'''
    i = 3
    sez = []
    while i + razmik <= 5:
        j = round((i + razmik), 2)
        sez.append(stevilo_z_oceno(i, j))
        i = round((i + razmik), 2)

    '''
    >>> razpored_knjig_ocena(0.25)
        Knjig z oceno med 3 in 3.25 je 9.
        Knjig z oceno med 3.25 in 3.5 je 68.
        Knjig z oceno med 3.5 in 3.75 je 263.
        Knjig z oceno med 3.75 in 4.0 je 585.
        Knjig z oceno med 4.0 in 4.25 je 660.
        Knjig z oceno med 4.25 in 4.5 je 303.
        Knjig z oceno med 4.5 in 4.75 je 74.
        Knjig z oceno med 4.75 in 5.0 je 31.
    '''

def graf():
    '''Izrise graf, ki pokaze koliksen delez
    knjig je na posameznem intervalu glede na oceno visjo od 3, za vzorec 3000 knjig.'''


    #Podatki
    labels = '3-3.25', '3.25-3.5', '3.5-3.75', '3.75-4.0', '4.0-4.25', '4.25-4.5', '4.5-4.75', '4.75-5.0'
    sizes = [9, 68, 263, 585, 660, 303, 74, 31]
    colors = ['gold', 'yellowgreen', 'yellow', 'green', 'lightcoral', 'lightskyblue', 'blue', 'red' ]
    explode = (0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05, 0.05)  #dele diagrama razsiri navzven

    #Plot
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)

    plt.axis('equal')
    plt.show()


            
def stevilo_knjig_na_crko():
    ''' vrne število knjig, katerih avtorji se začnejo na posamezno črko abecede. '''
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        knjige = []
        crke = list(string.ascii_uppercase)
        for crka in crke:
            koliko = 0
            stevec = 0
            with open('knjige21.csv', encoding='utf-8') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                for vrstica in csv_reader:
                    if stevec == 0:  # prve vrstice z imeni stolpcev ne štejemo
                        pass
                    elif len(vrstica) == 0:  # preskočimo prazne vrstice
                        pass
                    else:
                        if vrstica[1][0] == crka:
                            # vrstica[1][0] predstavlja prvo črko avtorja
                            koliko += 1 # če je ta enaka trenutni črki, povečamo koliko za 1
                    stevec += 1
            knjige.append((crka, koliko)) # v seznam knjige dodamo par (črka, število knjig na to črko)
        print(knjige)

    '''
    >>> stevilo_knjig_na_crko()
    [('A', 74), ('B', 35), ('C', 83), ('D', 64), ('E', 33), ('F', 3), ('G', 27), ('H', 20), ('I', 9), ('J', 152), ('K', 68), ('L', 41), ('M', 67),
    ('N', 41), ('O', 2), ('P', 41), ('Q', 0), ('R', 63), ('S', 107), ('T', 42), ('U', 2), ('V', 7), ('W', 10), ('X', 0), ('Y', 2), ('Z', 5)]
    '''

    
print('\n'
      'Pomoc uporabniku: Program analizira najbolj priljubljene knjige 21. '
      'stoletja, kot so predstavljene na spletni strani Goodreads.\n'
      '\n' 
      'Izberete lahko:\n'
      '\n'
      '-Funkcijo vrstice_naslovi_avtorji(), ki kot podatek prejme ime datoteke,' 
      'vrne pa stevilo vseh naslovov v datoteki s podatki in te naslove tudi izpise, vkljucno z njihovimi avtorji.\n'
      '\n' 
      '-Funkcija avtor_knjige() kot podatek prejme polno ime avtorja (brez narekovajev) in vrne podatek koliko njegovih del je v datoteki.\n'
      '\n' 
      '-Funkcija min_ocena() kot podatek prejme decimalno stevilo me 0 in 5, '
      'ki predstavlja oceno knjige. Izhod funkcije je seznam s podatki o knjigah z oceno visjo ali '
      'enako nasi izbrani.\n'
      '\n'
      '-Funkcija min_ocena_glasovi(ocena, glasovi) prejme za vhodne podatke oceno - decimalno stevilo in stevilo glasov,'
      'vrne pa seznam s podatki o knjigah, ki imajo hkrati oceno visjo od izbrane in je stevilo glasov vecje od zeljenega.\n'
      '\n'
      '-Funkcija stevilo_z_oceno() za podatka prejme decimalni stevili - spodnjo in zgornjo mejo ocen, med katerima zelimo,'
      'da so knjige ocenjene in vrne koliko je takih knjig.\n'
      '\n'
      '-Funkcija razpored_knjig_po_oceni() prejme kot podatek decimalno stevilo, ki predstavlja velikost intervala med ocenami. '
      'Vrne stevilo knjig na posameznem intervalu za ocene od 0 do 5.\n'
      '\n'
      '-Funkcija razpored_knjig_ocena() je enaka kot funkcija razpored_knjig_po_oceni(), ampak vrne samo podatke za dela med ocenama 3 in 5.\n'
      '\n'
      '-Ce vpisete "graf", vam bo prikazalo tortni diagram z delezi knjig na dolocenih intervalih ocen.\n'
      '\n'
      '-Funkcija stevilo_knjig_na_crko() vrne število knjig, katerih avtorji se začnejo na posamezno črko abecede.\n'
      '\n'
      'Za izhod vpisite "exit".'
      '\n')

vnos = [""]
while vnos[0] != "exit":
    vnos = input("Kaj vas zanima? ")
    vnos = vnos.split(')')[0].split('(')
    fun = vnos[0]
    if (len(vnos) > 1):
        args = vnos[1].split(',')

    if fun == 'vrstice_naslovi_avtorji':
        print(args)
        vrstice_naslovi_avtorji(str(args[0]))
    elif fun == 'avtor_knjige':
        avtor_knjige(args[0])
    elif fun == 'min_ocena':
        min_ocena(float(args[0]))
    elif fun == 'min_ocena_glasovi':
        min_ocena_glasovi(float(args[0]), int(args[1]))
    elif fun == 'stevilo_z_oceno':
        stevilo_z_oceno(float(args[0]), float(args[1]))
    elif fun == 'razpored_knjig_po_oceni':
        razpored_knjig_po_oceni(float(args[0]))
    elif fun == 'razpored_knjig_ocena':
        razpored_knjig_ocena(float(args[0]))
    elif fun == 'stevilo_knjig_na_crko':
        stevilo_knjig_na_crko()
    elif fun == 'graf':
        graf()


