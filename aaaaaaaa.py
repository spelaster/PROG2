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
