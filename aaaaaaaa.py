import csv
import json
import re
import orodja

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
    #naslov
    r'aria-level=\'4\'>(?P<naslov>[^<|(]*[^ |(|<]).*?'
    #avtor
    r'<span itemprop="name">(?P<avtor>.*?)</span>.*?'
    #povprečna ocena
    r' (?P<ocena>\d{1}\.\d{2}) avg rating.*?'
    #ocena na podlagi števila glasovalcev in njihovih ocen
    #r'(?P<score>.*?).*?'
    r'score: (?P<score>.*?)</a>.*?'
    #stevilo glasovalcev
    r'>(?P<glasovalci>[\d|,]*) people voted.*?',
    re.DOTALL
)
                                                                      

def cisti_podatki(podatki):
    podatki_knjige = podatki.groupdict()
    podatki_knjige['ocena'] = float(podatki_knjige['ocena'].replace(',', '.'))
    podatki_knjige['naslov'] = str(podatki_knjige['naslov'].replace('&quot;','"'))
    podatki_knjige['score'] = float(podatki_knjige['score'].replace(',', '.'))
    podatki_knjige['glasovalci'] = int(podatki_knjige['glasovalci'].replace(',', ''))
    return podatki_knjige

for i in range(1, 11):
    url = ('https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page={}').format(i)
    orodja.shrani_spletno_stran(url, 'stran-{}.html'.format(i))

podatki = []
for stran in range(1,11):
    vsebina = orodja.vsebina_datoteke('stran-{}.html'.format(stran))
    for ujemanje in vzorec.finditer(vsebina):
        podatki_knjige = cisti_podatki(ujemanje)
        podatki.append(podatki_knjige)
zapisi_csv(podatki, ['naslov', 'avtor', 'ocena', 'score', 'glasovalci'], 'knjige21.csv')
zapisi_json(podatki, 'knjige.json')

print("&quot;A Problem from Hell&quot;: America and the Age of Genocide")



def izpisi_naslove_in_avtorje(dat):
    stevec = 0
    with open(dat, encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        stevec = 0
        for vrstica in csv_reader:

            if stevec == 0:
                print(f'Imena stolpcev so {", ".join(vrstica)}')
                pass
            if len(vrstica) == 0:
                pass          
            else:
                naslov = vrstica[0]
                avtor = vrstica[1]
                ocena = vrstica[2]
                score = vrstica[3]
                glasovalci = vrstica[4]
                print(f'\t naslov: {vrstica[0]}, avtor: {vrstica[1]}.')
                stevec += 1
        print(f'Nasa datoteka ima {stevec} vrstic s podatki o knjigah.')

def avtor_knjige(avtor):
    stevec = 0
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        koliko = 0
        naslovi = []
        for vrstica in csv_reader:
            if len(vrstica) == 0:
                pass          
            else:
                if vrstica[1] == avtor: # če je avtor dela enak avtorju trenutne vrstice
                    naslovi.append(vrstica[0]) # dodamo naslov knjige k naslovom njegovih del
                    koliko += 1
        nas = ', '.join(naslovi)
        kdo = str(avtor)
        if koliko == 0:
            print(f'Avtor/ica {kdo} ni napisal/a nobenega dela, ki je v datoteki "knjige21.csv".')
        elif koliko == 1:
            print(f'Avtor/ica {kdo} je napisal/a eno delo z naslovom {nas}, ki je v datoteki "knjige21.csv".')
        elif koliko == 2:
            print(f'Avtor/ica {kdo} je napisal/a dve deli z naslovoma {nas}, ki sta v datoteki "knjige21.csv".')
        else:
            print(f'Avtor/ica {kdo} je napisal/a {koliko} del z naslovi: {nas}, ki so v datoteki "knjige21.csv"')

        '''
            >>> avtor_knjige("J.K. Rowling")
            Avtor/ica J.K. Rowling je napisal/a 5 del z naslovi: Harry Potter and the Deathly Hallows,
            Harry Potter and the Half-Blood Prince, Harry Potter and the Order of the Phoenix,
            The Tales of Beedle the Bard, The Casual Vacancy.

            >>> avtor_knjige("Enid Bliton")
            Avtor/ica Enid Bliton ni napisal/a nobenega dela.

            >>> avtor_knjige("Markus Zusak")
            Avtor/ica Markus Zusak je napisal/a dve deli z naslovoma The Book Thief, I Am the Messenger, ki sta v datoteki "knjige21.csv".
        '''

def izpisi_knjige_z_oceno_vsaj(ocena):
    ''' Funkcija izpiše naslove, avtorje ter oceno knjig, ki imajo oceno enako ali višjo vnešeni oceni. '''
    stevec = 0
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        stevec = 0
        knjige = []
        for vrstica in csv_reader:
            if stevec == 0: # prve vrstice z imeni stolpcev ne štejemo 
                pass
            elif len(vrstica) == 0: # preskočimo prazne vrstice
                pass          
            else:
                if float(vrstica[2]) >= float(ocena): # če je ocena višja ali enaka željeni oceni
                    knjige.append((vrstica[0], vrstica[1], vrstica[2])) # dodamo naslov, avtorja in oceno v seznam 
            stevec += 1
        print(f'Knjige z oceno, višjo ali enako {ocena}, so: {knjige}.')

    '''
        >>> izpisi_knjige_nad_oceno(4.6)
        Knjige z oceno, višjo ali enako 4.6, so: [('Harry Potter and the Deathly Hallows', 'J.K. Rowling', '4.62'), ('Una Historia de Ayer', 'Sergio Cobo', '4.64'),
        ('The Way of Kings', 'Brandon Sanderson', '4.65'), ('Meeting With Christ and Other Poems', 'Deepak Chaswal', '4.6'),
        ('TIME TRAVEL EXPERIENCES: In a Sense, we all are Time Travelers! We are surviving each and every Active Time-Point in this Timeline.......', 'Aldrin Mathew', '4.8'),
        ('A Court of Mist and Fury', 'Sarah J. Maas', '4.65'), ('Speedy Reads', 'Chris-Jean Clarke', '4.74'), ('The Code: The Assiduous Quest of Tobias Hopkins - Part Two', 'James Faro', '4.86'),
        ('Trueman Bradley - The Next Great Detective', 'Alexei Maxim Russell', '4.75'), ('Laços fortes e decisões difíceis', 'Graça Jacinto', '4.73'),
        ('Never Go With Your Gut: How Pioneering Leaders Make the Best Decisions and Avoid Business Disasters', 'Gleb Tsipursky', '4.65'), ('The Years Distilled: Verses', 'Dennis Sharpe', '4.87'),
        ('Words of Radiance', 'Brandon Sanderson', '4.76'), ("Regular People of The Weak: A Rebel's Experience With The Spiritual Chief of Poets", 'Shareef Mabrouk', '4.78'),
        ("I'm Unapologetically Single And More Than OK With It", 'Justin Ho', '5.0'), ('The Tainted Trust', 'Stephen Douglass', '4.65'), ('Goals, Obstacles And Gratitude', 'Justin Ho', '5.0'),
        ('10% Everything', 'Justin Ho', '5.0'), ('Self-Improvement And Success', 'Justin Ho', '5.0'), ('Life Amplifiers Daily Devotional', 'Justin Ho', '5.0'),
        ('Dream Big, Live Bigger', 'Justin Ho', '5.0'), ('Self-Esteem - Self = Esteem', 'Justin Ho', '5.0'), ('The Fish the Fighters and the Song-Girl', 'Janet E. Morris', '4.62'),
        ('The Old Has Gone, The New Is Here', 'Justin Ho', '5.0'), ('How To Develop A Million Dollar Mindset', 'Justin Ho', '5.0'), ('Stop Auto-Piloting', 'Justin Ho', '5.0'),
        ('Your Skill, Your Wealth Builder', 'Justin Ho', '5.0')].


        >>> izpisi_knjige_z_oceno_vsaj(5)
        Knjige z oceno, višjo ali enako 5, so: [("I'm Unapologetically Single And More Than OK With It", 'Justin Ho', '5.0'), ('Goals, Obstacles And Gratitude', 'Justin Ho', '5.0'),
        ('10% Everything', 'Justin Ho', '5.0'), ('Self-Improvement And Success', 'Justin Ho', '5.0'), ('Life Amplifiers Daily Devotional', 'Justin Ho', '5.0'),
        ('Dream Big, Live Bigger', 'Justin Ho', '5.0'), ('Self-Esteem - Self = Esteem', 'Justin Ho', '5.0'), ('The Old Has Gone, The New Is Here', 'Justin Ho', '5.0'),
        ('How To Develop A Million Dollar Mindset', 'Justin Ho', '5.0'), ('Stop Auto-Piloting', 'Justin Ho', '5.0'), ('Your Skill, Your Wealth Builder', 'Justin Ho', '5.0')].
        '''

# če upoštevamo še glasove, dobimo malo drugačno sliko:
def izpisi_knjige_z_oceno_vsaj(ocena, glasovi):
    ''' Funkcija izpiše naslove, avtorje, oceno in število glasov knjig,
        ki imajo oceno enako ali višjo vnešeni oceni in zadostno število glasov. '''
    stevec = 0
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        stevec = 0
        knjige = []
        for vrstica in csv_reader:
            if stevec == 0: # prve vrstice z imeni stolpcev ne štejemo 
                pass
            elif len(vrstica) == 0: # preskočimo prazne vrstice
                pass          
            else:
                if (float(vrstica[2]) >= float(ocena)) and (float(vrstica[4]) >= float(glasovi)):
                    # če je ocena višja ali enaka željeni oceni in je število glasov zadostno
                    knjige.append((vrstica[0], vrstica[1], vrstica[2], vrstica[4])) # dodamo naslov, avtorja, oceno in glasove v seznam 
            stevec += 1
        print(f'Knjige z oceno, višjo ali enako {ocena}, in z vsaj {glasovi} glasovi so: {knjige}.')

        '''
        >>> izpisi_knjige_z_oceno_vsaj(4.6, 100)
        Knjige z oceno, višjo ali enako 4.6, in z vsaj 100 glasovi so: [('Harry Potter and the Deathly Hallows', 'J.K. Rowling', '4.62', '3993'),
        ('Una Historia de Ayer', 'Sergio Cobo', '4.64', '130')].
        '''



def stevilo_z_oceno(ocena_spodaj, ocena_zgoraj):
    ''' vrne število knjig, ki se nahajajo med določenima ocenama - od spodnje do vključno zgornje). '''
    stevec = 0
    with open('knjige21.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        stevec = 0
        koliko = 0
        knjige = []
        for vrstica in csv_reader:
            if stevec == 0: # prve vrstice z imeni stolpcev ne štejemo 
                pass
            elif len(vrstica) == 0: # preskočimo prazne vrstice
                pass          
            else:
                if (float(vrstica[2]) > float(ocena_spodaj)) and (float(vrstica[2]) <= float(ocena_zgoraj)):
                    # če je ocena višja od ocena_spodaj in nižja ali enaka ocena_zgoraj
                    # knjige.append((vrstica[0], vrstica[1], vrstica[2])) # dodamo naslov, avtorja in oceno v seznam
                    koliko += 1
            stevec += 1
        print(f'Knjig z oceno med {ocena_spodaj} in {ocena_zgoraj} je {koliko}.')


        '''
        >>> stevilo_z_oceno(4, 4.6)
        Knjig z oceno med 4 in 4.6 je 492.
        '''

def razpored_knjig_po_oceni(razmik):
    ''' Vrne koliko knjig se nahaja med določenima ocenama, ocene so razporejene po danem razmaku.
        Upoštevamo, da je najvišja ocena enaka 5. '''
    i = 0
    sez = []
    while i + razmik <=5:
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
    Knjig z oceno med 2.5 in 3.0 je 0.
    Knjig z oceno med 3.0 in 3.5 je 36.
    Knjig z oceno med 3.5 in 4.0 je 446.
    Knjig z oceno med 4.0 in 4.5 je 475.
    Knjig z oceno med 4.5 in 5.0 je 43.

    Vidimo, da z oceno, manjšo od 3.0, ni ocenjena nobena knjiga.
    '''

def razpored_knjig_ocena(razmik):
    ''' Vrne koliko knjig se nahaja med določenima ocenama, ocene so razporejene po danem razmaku.
        Upoštevamo, da je najnižja ocena enaka 3 in najvišja ocena enaka 5.'''
    i = 3
    sez = []
    while i + razmik <=5:
        j = round((i + razmik),2)
        sez.append(stevilo_z_oceno(i, j))
        i = round((i + razmik),2)

    '''
    >>> razpored_knjig_ocena(0.1)
    Knjig z oceno med 3 in 3.1 je 2.
    Knjig z oceno med 3.1 in 3.2 je 1.
    Knjig z oceno med 3.2 in 3.3 je 5.
    Knjig z oceno med 3.3 in 3.4 je 6.
    Knjig z oceno med 3.4 in 3.5 je 22.
    Knjig z oceno med 3.5 in 3.6 je 30.
    Knjig z oceno med 3.6 in 3.7 je 60.
    Knjig z oceno med 3.7 in 3.8 je 74.
    Knjig z oceno med 3.8 in 3.9 je 120.
    Knjig z oceno med 3.9 in 4.0 je 162.
    Knjig z oceno med 4.0 in 4.1 je 159.
    Knjig z oceno med 4.1 in 4.2 je 120.
    Knjig z oceno med 4.2 in 4.3 je 93.
    Knjig z oceno med 4.3 in 4.4 je 68.
    Knjig z oceno med 4.4 in 4.5 je 35.
    Knjig z oceno med 4.5 in 4.6 je 17.
    Knjig z oceno med 4.6 in 4.7 je 7.
    Knjig z oceno med 4.7 in 4.8 je 6.
    Knjig z oceno med 4.8 in 4.9 je 2.
    Knjig z oceno med 4.9 in 5.0 je 11.


    >>> razpored_knjig_ocena(0.25)
    Knjig z oceno med 3 in 3.25 je 6.
    Knjig z oceno med 3.25 in 3.5 je 30.
    Knjig z oceno med 3.5 in 3.75 je 126.
    Knjig z oceno med 3.75 in 4.0 je 320.
    Knjig z oceno med 4.0 in 4.25 je 322.
    Knjig z oceno med 4.25 in 4.5 je 153.
    Knjig z oceno med 4.5 in 4.75 je 27.
    Knjig z oceno med 4.75 in 5.0 je 16.
    '''

##import matplotlib.pyplot as plt
##
### Data to plot
##labels = '3-3.25', '3.25-3.5', '3.5-3.75', '3.75-4.0', '4.0-4.25', '4.25-4.5', '4.5-4.75', '4.75-5.0'
##sizes = [6, 30, 126, 320, 322, 153, 27, 16]
##colors = ['gold', 'yellowgreen', 'yellow', 'green', 'lightcoral', 'lightskyblue', 'blue' ]
##explode = (0.1, 0, 0, 0, 0, 0, 0)  # explode 1st slice
##
### Plot
##plt.pie(sizes, explode=explode, labels=labels, colors=colors,
##autopct='%1.1f%%', shadow=True, startangle=140)
##
##plt.axis('equal')
##plt.show()


        
