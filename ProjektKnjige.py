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
    r'<a title="(?P<naslov>[^"|(]*[^ |"|(]).*?'
    r'<span itemprop="name">(?P<avtor>.+?)</span></a>.*?'
    r'avg rating (?P<ocena>\d{1}\.\d{2}) —.*?'
    r'published (?P<leto>\d{4}).*?</span>',
    re.DOTALL
)

def cisti_podatki(podatki):
    podatki_knjige = podatki.groupdict()
    podatki_knjige['leto'] = int(podatki_knjige['leto'])
    podatki_knjige['ocena'] = float(podatki_knjige['ocena'].replace(',', '.'))
    return podatki_knjige

podatki = []
vsebina = orodja.vsebina_datoteke('knjige21.html')
for ujemanje in vzorec.finditer(vsebina):
    podatki_knjige = cisti_podatki(ujemanje)
    podatki.append(podatki_knjige)
zapisi_csv(podatki, ['naslov', 'avtor', 'leto', 'ocena'], 'knjige21.csv')
zapisi_json(podatki, 'filmi.json')