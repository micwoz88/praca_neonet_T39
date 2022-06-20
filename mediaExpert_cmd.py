from re import I
import funkcje as f

f.adres_url = 'https://www.mediaexpert.pl'
kod_zrodlowy = f.pobierz_kod_selenium(f.adres_url,30,screen=True)

#---------------------------------------------------------------------------------------
#--------------------------top baner----------------------------------------------------
#---------------------------------------------------------------------------------------
top_banner_tytuly = kod_zrodlowy.find(id='section_carousel-pagination').find_all('a')
top_bannery_img = kod_zrodlowy.find(id='section_carousel-banner').find_all('img')

for ban in range(0,len(top_banner_tytuly)):
    tytul = top_banner_tytuly[ban].text.strip()
    adres = f.dodaj_https(top_banner_tytuly[ban]['href'])
    podstrona = f.pobierz_kod_selenium(adres)
    if podstrona.find(class_='sg_ft_in'):
        #------------------------------------------------------------
        wynik = podstrona.find(class_='sg_ft_in')
        try:
            regulamin = wynik.find_all('a')[0]['href']
            if regulamin == 'https://www.mediaexpert.pl':
                regulamin = ''
            czas_trwania = wynik.get_text()[wynik.get_text().find('Akcja') - 1:wynik.get_text().find(' lub do')].strip()
            if len(czas_trwania) > 300:
                czas_trwania = ''
        #------------------------------------------------------------  
        except:
            czas_trwania = ''
            regulamin = ''
    else:
        czas_trwania = ''
        regulamin = ''
    f.dodaj_rekord(tytul,adres,1,czas_trwania=czas_trwania,regulamin=regulamin)

    adres_img = top_bannery_img[ban]['src']

    roz_img = f.rozszerzenie_img(adres_img)
    adres_img = f.dodaj_https(adres_img)
    
    f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
    ban_img = f.Image.open(f'img/{f.nr_banera}.{roz_img}')
    width, height = ban_img.size

    im = ban_img.crop((600,0,width-300,height))
    if roz_img == 'jpg':
        typ = 'jpeg'
    else:
        typ = roz_img
    im.save(f'img/{f.nr_banera}.{roz_img}',typ)

    f.konwertuj_do_png(f.nr_banera,roz_img)

    print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------baner II rzad------------------------------------------------
#---------------------------------------------------------------------------------------
baner_rzad_2 = kod_zrodlowy.find(id='section_banners-top').find_all(class_='spark-link')

# banner lewy
adres = f.dodaj_https(baner_rzad_2[0]['href'])
podstrona = f.pobierz_kod_selenium(adres)
tytul = podstrona.title.get_text()
# if not(tytul.find('Promocje Media Expert') == - 1):
#     tytul = tytul[0:tytul.find('Promocje Media Expert') - 3]
if podstrona.find(class_='sg_ft_in'):
    #------------------------------------------------------------
    wynik = podstrona.find(class_='sg_ft_in')
    try:
        regulamin = wynik.find_all('a')[0]['href']
        if regulamin == 'https://www.mediaexpert.pl':
                regulamin = ''
        czas_trwania = wynik.get_text()[wynik.get_text().find('Akcja') - 1:wynik.get_text().find(' lub do')].strip()
        if len(czas_trwania) > 300:
                czas_trwania = ''
    #------------------------------------------------------------  
    except:
        czas_trwania = ''
        regulamin = ''
else:
    czas_trwania = ''
    regulamin = ''
f.dodaj_rekord(tytul,adres,2,czas_trwania=czas_trwania,regulamin=regulamin)

adres_img = f.dodaj_https(baner_rzad_2[0].find('picture').find('source')['srcset'])
roz_img = f.rozszerzenie_img(adres_img)
f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
f.konwertuj_do_png(f.nr_banera,roz_img)

print(f'baner - {f.nr_banera} - jest')


# banner prawy - oferta dnia
try:
    adres = f.dodaj_https(baner_rzad_2[1]['href'])
    podstrona = f.pobierz_kod_selenium(adres)
    tytul = 'Oferta dnia! - Promocje Media Expert'
    #dodaj podtytul
    podtytul = podstrona.find(class_='product_title l').get_text().strip()
    
    data_waznosci = f'Promocyjną cenę gwarantujemy w dniu {f.data.day}.{f.data.month}.{f.data.year} r. w godzinach 00:00 – 23:59'
    f.dodaj_rekord(tytul,adres,2,podtytul,data_waznosci)

    ban_img = f.Image.open(f'img/{f.nazwa_sklepu}.png')
    # im = ban_img.crop((800,627,800 + 665,627 + 400))
    im = ban_img.crop((800,1346,800 + 665,1346 + 400))
    im.save(f'img/{f.nr_banera}.png','png')
except:
    tytul = 'Oferty dnia'
    f.dodaj_rekord(tytul)
    print('nie pobrałem oferty dnia')
print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------baner III rzad-----------------------------------------------
#---------------------------------------------------------------------------------------
baner_rzad_3 = kod_zrodlowy.find(id='section_banners-bottom').find_all(class_='banner-box-small')

for ban in range(0, len(baner_rzad_3)):
    adres = f.dodaj_https(baner_rzad_3[ban].a['href'])
    podstrona = f.pobierz_kod_selenium(adres)
    tytul = podstrona.title.get_text()
    if not(tytul.find('Promocje Media Expert') == - 1):
        tytul = tytul[0:tytul.find('Promocje Media Expert') - 3]
    if podstrona.find(class_='sg_ft_in'):
        #------------------------------------------------------------
        wynik = podstrona.find(class_='sg_ft_in')
        try:
            regulamin = wynik.find_all('a')[0]['href']
            if regulamin == 'https://www.mediaexpert.pl':
                regulamin = ''
            czas_trwania = wynik.get_text()[wynik.get_text().find('Akcja') - 1:wynik.get_text().find(' lub do')].strip()
            if len(czas_trwania) > 300:
                czas_trwania = ''
        #------------------------------------------------------------  
        except:
            czas_trwania = ''
            regulamin = ''
    else:
        czas_trwania = ''
        regulamin = ''
    f.dodaj_rekord(tytul,adres,2,czas_trwania=czas_trwania,regulamin=regulamin)

    adres_img = f.dodaj_https(baner_rzad_3[ban].find('picture').find('source')['srcset'])
    roz_img = f.rozszerzenie_img(adres_img)
    f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
    f.konwertuj_do_png(f.nr_banera,roz_img)

    print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------reszta-------------------------------------------------------
#---------------------------------------------------------------------------------------
try:
    baner_rzad_4 = kod_zrodlowy.find(id='banners_tiles_section1-main').find_all(class_='content')

    for ban in range(0, len(baner_rzad_4)):
        adres = f.dodaj_https(baner_rzad_4[ban].a['href'])
        podstrona = f.pobierz_kod_selenium(adres)
        tytul = podstrona.title.get_text()
        if not(tytul.find('Promocje Media Expert') == - 1):
            tytul = tytul[0:tytul.find('Promocje Media Expert') - 3]
        if podstrona.find(class_='sg_ft_in'):
            #------------------------------------------------------------
            wynik = podstrona.find(class_='sg_ft_in')
            try:
                regulamin = wynik.find_all('a')[0]['href']
                if regulamin == 'https://www.mediaexpert.pl':
                    regulamin = ''
                czas_trwania = wynik.get_text()[wynik.get_text().find('Akcja') - 1:wynik.get_text().find(' lub do')].strip()
                if len(czas_trwania) > 300:
                    czas_trwania = ''
            #------------------------------------------------------------  
            except:
                czas_trwania = ''
                regulamin = ''
        else:
            czas_trwania = ''
            regulamin = ''
        f.dodaj_rekord(tytul,adres,2,czas_trwania=czas_trwania,regulamin=regulamin)

        adres_img = f.dodaj_https(baner_rzad_4[ban].find('picture').find('source')['srcset'])
        roz_img = f.rozszerzenie_img(adres_img)
        f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
        f.konwertuj_do_png(f.nr_banera,roz_img)

        print(f'baner - {f.nr_banera} - jest')
        
except:
    pass

#---------------------------------------------------------------------------------------
banner_reszta = kod_zrodlowy.find(id='section_banners-products').find_all(class_='banner-product')

for i in range(0,len(banner_reszta)):
    if bool(banner_reszta[i].find(class_='list')):
        ban = banner_reszta[i].find_all(class_='list')
        for j in range(0,len(ban)):
            linki = ban[j].find_all('a')
            for k in range(0,len(linki)):
                adres = f.dodaj_https(linki[k]['href'])
                podstrona = f.pobierz_kod_selenium(adres)
                tytul = podstrona.title.get_text()
                if not(tytul.find('Promocje Media Expert') == - 1):
                    tytul = tytul[0:tytul.find('Promocje Media Expert') - 3]
                if podstrona.find(class_='sg_ft_in'):
                    #------------------------------------------------------------
                    wynik = podstrona.find(class_='sg_ft_in')
                    try:
                        regulamin = wynik.find_all('a')[0]['href']
                        if regulamin == 'https://www.mediaexpert.pl':
                            regulamin = ''
                        czas_trwania = wynik.get_text()[wynik.get_text().find('Akcja') - 1:wynik.get_text().find(' lub do')].strip()
                        if len(czas_trwania) > 300:
                            czas_trwania = ''
                    #------------------------------------------------------------  
                    except:
                        czas_trwania = ''
                        regulamin = ''
                else:
                    czas_trwania = ''
                    regulamin = ''
                f.dodaj_rekord(tytul,adres,2,czas_trwania=czas_trwania,regulamin=regulamin)

                print(f'baner - {f.nr_banera} - jest - bez img')
                
    else:
        ban = banner_reszta[i].find_all(class_='banner')
        for j in range(0,len(ban)):
            linki = ban[j].find_all('a')
            for k in range(0,len(linki)):
                adres = f.dodaj_https(linki[k]['href'])
                podstrona = f.pobierz_kod_selenium(adres)
                tytul = podstrona.title.get_text()
                if not(tytul.find('Promocje Media Expert') == - 1):
                    tytul = tytul[0:tytul.find('Promocje Media Expert') - 3]
                if podstrona.find(class_='sg_ft_in'):
                    #------------------------------------------------------------
                    wynik = podstrona.find(class_='sg_ft_in')
                    try:
                        regulamin = wynik.find_all('a')[0]['href']
                        if regulamin == 'https://www.mediaexpert.pl':
                            regulamin = ''
                        czas_trwania = wynik.get_text()[wynik.get_text().find('Akcja') - 1:wynik.get_text().find(' lub do')].strip()
                        if len(czas_trwania) > 300:
                            czas_trwania = ''
                    #------------------------------------------------------------  
                    except:
                        czas_trwania = ''
                        regulamin = ''
                else:
                    czas_trwania = ''
                    regulamin = ''
                f.dodaj_rekord(tytul,adres,2,czas_trwania=czas_trwania,regulamin=regulamin)
                
                adres_img = f.dodaj_https(linki[k].find('picture').find('source')['srcset'])
                roz_img = f.rozszerzenie_img(adres_img)
                f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
                f.konwertuj_do_png(f.nr_banera,roz_img)

                print(f'baner - {f.nr_banera} - jest')

#--------------------------------------------------------------------------------------------------
f.zapisz_dane_do_docx(f.nazwa_sklepu)