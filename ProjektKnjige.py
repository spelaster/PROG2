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
    r"aria-level='4'>(?P<naslov>[^<|(]*[^ |(|<]).*?"
    #avtor
    r'<span itemprop="name">(?P<avtor>.*?)</span>.*?'
    #povprečna ocena
    r' (?P<ocena>\d{1}\.\d{2}) avg rating.*?'
    #ocena na podlagi števila glasovalcev in njihovih ocen
    r'score: (?P<score>.*?)</a>.*?'
    #stevilo glasovalcev
    r'>(?P<glasovalci>[\d|,]*) people voted.*?',
    re.DOTALL
)

def cisti_podatki(podatki):
    podatki_knjige = podatki.groupdict()
    podatki_knjige['ocena'] = float(podatki_knjige['ocena'].replace(',', '.'))
    podatki_knjige['score'] = float(podatki_knjige['score'].replace(',', '.'))
    podatki_knjige['glasovalci'] = int(podatki_knjige['glasovalci'].replace(",", ""))
    return podatki_knjige

for i in range(1, 11):
    url = ('https://www.goodreads.com/list/show/7.Best_Books_of_the_21st_Century?page={}').format(i)
    orodja.shrani_spletno_stran(url, 'stran-{}.html'.format(i))

podatki = []
vsebina = orodja.vsebina_datoteke('knjige21.html')
for ujemanje in vzorec.finditer(vsebina):
    podatki_knjige = cisti_podatki(ujemanje)
    print(podatki_knjige)
    podatki.append(podatki_knjige)
zapisi_csv(podatki, ['naslov', 'avtor', 'ocena', 'score', 'glasovalci'], 'knjige21.csv')
zapisi_json(podatki, 'knjige.json')
