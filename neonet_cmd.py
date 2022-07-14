import funkcje as f

def podaj_czas(podstrona):
    try:
        pattern_termin = f.re.compile(r'(Promoc(ja|yjną)|Akcja).{,200}(obowiązuje|trwa)?.{,200}do.{,200}(\d\d:\d\d|\d\d\.\d\d\.\d\d\d\d r\.)', f.re.S)
        czas = pattern_termin.search(str(podstrona))
        czas = str(podstrona)[czas.start():czas.end()]
        czas = f.re.sub(r'[ ]?(<|</)b>[ ]?', ' ', czas)
        czas = f.re.sub(r'\n', ' ', czas)
        czas = f.re.sub(r' ,', ',', czas)
        pattern_tag = f.re.compile('<.*?>')
        czas = pattern_tag.sub('', czas)
    except:
        czas = ''
    return czas

def podaj_regulamin(podstrona):
    try:
        pattern_reg_link = f.re.compile(r'(http|/)\S*?\.pdf')
        regulamin_link = pattern_reg_link.search(str(podstrona))
        regulamin_link = str(podstrona)[regulamin_link.start():regulamin_link.end()]
        regulamin_link = f.dodaj_https(regulamin_link)
        pomin = ['https://www.neonet.pl/images24/promocje/2022/listy/Regulamin-opinii-V4_po-uwzglednieniu-poprawek.pdf']
        for link in pomin:
            if link == regulamin_link:
                regulamin_link = ''
    except:
        regulamin_link = ''
    return regulamin_link

f.adres_url = 'https://www.neonet.pl'
kod_zrodlowy = f.pobierz_kod_selenium(f.adres_url,15,True)

#---------------------------------------------------------------------------------------
#--------------------------top banner---------------------------------------------------
#---------------------------------------------------------------------------------------
top_banner_sekcja = kod_zrodlowy.find(class_='heroHomeCss-root-1M1').find_all(class_='singleSlideCss-root-Jgr')
for ban in range(0,len(top_banner_sekcja)):
    adres = f.dodaj_https(top_banner_sekcja[ban].find('a')['href'])
    nie_ma = True
    for rekord in f.dane:
        if rekord[3] == adres:
            nie_ma = False

    if nie_ma:
        podstrona = f.pobierz_kod_selenium(adres,6)  
        czas = podaj_czas(podstrona)
        regulamin_link = podaj_regulamin(podstrona)

        img = top_banner_sekcja[ban].find('img')
        tytul = img['alt']
        f.dodaj_rekord(tytul,adres,1,czas_trwania=czas,regulamin=regulamin_link)
        f.zapisz_grafike(img['src'],'webp',f.nr_banera)
        f.konwertuj_webp_to_png(f.nr_banera)

        print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------promocje-----------------------------------------------------
#---------------------------------------------------------------------------------------
sekcje = kod_zrodlowy.find(id='homepageContent')
promocje_sekcja = sekcje.find_all('section')

try:
    tytul_sekcji = promocje_sekcja[0].find('h2').get_text()
    f.dodaj_rekord(tytul_sekcji)

    promocje_sekcja = promocje_sekcja[0].find(class_='homePromotionsCss-root-1xS')
    linki = promocje_sekcja.find_all('a')
    img = promocje_sekcja.find_all('img')

    dodane = []
    typ_banera = 1
    for ban in range(0,len(linki)):
        tytul = img[ban]['alt']
        adres = f.dodaj_https(linki[ban]['href'])
        podstrona = f.pobierz_kod_selenium(adres,6)
        czas = podaj_czas(podstrona)
        regulamin_link = podaj_regulamin(podstrona)

        if adres in dodane:
            typ_banera = 2
        dodane.append(adres)

        f.dodaj_rekord(tytul,adres,typ=typ_banera,czas_trwania=czas,regulamin=regulamin_link)
        f.zapisz_grafike(img[ban]['src'],'webp',f.nr_banera)
        f.konwertuj_webp_to_png(f.nr_banera)

        print(f'baner - {f.nr_banera} - jest')
except:
    f.dodaj_rekord('error')
    print('error')

#---------------------------------------------------------------------------------------
f.zapisz_dane_do_docx('neonet')