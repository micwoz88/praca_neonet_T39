import funkcje as f

f.adres_url = 'https://www.euro.com.pl'
okno = f.webdriver.Firefox()
okno.get(f.adres_url)
okno.implicitly_wait(10)
okno.find_element_by_id('onetrust-accept-btn-handler').click()
wysokosc_strony = okno.execute_script("return document.body.scrollHeight")
okno.set_window_size(1600,wysokosc_strony + 8000)

f.time.sleep(10)
okno.minimize_window()

kod_zrodlowy = f.BeautifulSoup(str(okno.page_source), features='html.parser')

#---------------------------------------------------------------------------------------
#--------------------------top baner----------------------------------------------------
#---------------------------------------------------------------------------------------
top_banner_all = kod_zrodlowy.find(id='main-page-top-slider')

top_banner_tytuly = top_banner_all.find_all(class_='slider-button')
top_banner = top_banner_all.find(class_='slider-list').find_all(class_='slider-content')

wys_top = okno.find_element_by_id('top').size.get('height')
wys_top_menu = okno.find_element_by_id('main-menu').size.get('height')
wys_top_slider = okno.find_element_by_id('main-page-top-slider').size.get('height')
try:
    wys_hity = okno.find_element_by_id('top-product-rotator').size.get('height')
except:
    wys_hity = 0
wys_main = okno.find_element_by_class_name('page').size.get('height')
wys_stopka = okno.find_element_by_id('main-footer').size.get('height')

okno.set_window_size(1600,wys_top + wys_top_menu + wys_top_slider + 39)
f.time.sleep(5)
okno.minimize_window()

for i in range(len(top_banner_tytuly)):
    tytul = top_banner_tytuly[i].text.strip()
    adres = f.dodaj_https(top_banner[i].a['href'])
    f.dodaj_rekord(tytul,adres,1)
    f.pobierz_info_promo_euro(adres)

    okno.save_screenshot(f'img/{f.nr_banera}.png')

    img = f.Image.open(f'img/{f.nr_banera}.png')
    szer, wys = img.size
    im = img.crop((35,wys_top + wys_top_menu,35 + (szer - 100),wys_top + wys_top_menu + (wys - wys_top - wys_top_menu)))
    im.save(f'img/{f.nr_banera}.png','png')
    print(f'baner - {f.nr_banera} - jest')
    
    okno.find_element_by_css_selector('.slider-next > button:nth-child(1)').click()
    f.time.sleep(5)

#---------------------------------------------------------------------------------------
#--------------------------hity dnia----------------------------------------------------
#---------------------------------------------------------------------------------------
try:
    hity_banner = kod_zrodlowy.find(id='top-product-header').find('a')

    print('\nHity dnia')

    adres = f.dodaj_https(hity_banner['href'])
    podstrona = f.pobierz_kod_Beauti(adres)
    tylul = podstrona.find('title').get_text()
    f.dodaj_rekord(tylul,adres)
    f.pobierz_info_promo_euro(adres)

    okno.execute_script(f"window.scrollTo(0, {wys_top_menu + wys_top_slider + 57});")
    f.time.sleep(5)
    okno.save_screenshot('img/top_hit_usl.png')

    img = f.Image.open('img/top_hit_usl.png')
    szer, wys = img.size
    im = img.crop((184,wys_top - 39,180 + (szer - 378),wys_top - 39 + 255))
    im.save(f'img/{f.nr_banera}.png','png')

    print(f'baner - {f.nr_banera} - jest')

except:
    print('\nHity dnia')
    print('\nError')

#---------------------------------------------------------------------------------------
#--------------------------usugi--------------------------------------------------------
#---------------------------------------------------------------------------------------
uslugi_bannery = kod_zrodlowy.find(id='horizontal-banners').find_all(class_='banner-item')

print('\nUsługi')

try:
    img_usl = f.Image.open('img/top_hit_usl.png')
    szer, wys = img_usl.size
    im = img_usl.crop((184,wys_top + wys_hity - 20,180 + (szer - 378),wys_top + wys_hity - 110 + 255))
    im.save('img/top_hit_usl.png','png')

    img_usl = f.Image.open('img/top_hit_usl.png')
    szer, wys = img_usl.size

    for banner in range(1,len(uslugi_bannery)):
        try:
            if banner == 1:
                item = f'uspItem'
                ban = uslugi_bannery[banner].find(class_=item).find(class_=f'{item}__textContainer')
                adres = f.dodaj_https(ban.find(class_=f'{item}__heading')['href'])
                tytul = ban.find(class_=f'{item}__heading').get_text().strip()
                f.dodaj_rekord(tytul,adres)
                # pierwszy banner
                im = img_usl.crop((0, 0, szer - 610, wys))
                im.save(f'img/{f.nr_banera}.png','png')
                print(f'baner - {f.nr_banera} - jest')
            else:
                item = f'uspItemV{banner}'
                ban = uslugi_bannery[banner].find(class_=item).find(class_=f'{item}__textContainer')
                adres = f.dodaj_https(ban.find(class_=f'{item}__heading')['href'])
                tytul = ban.find(class_=f'{item}__heading').get_text().strip()
                f.dodaj_rekord(tytul,adres)
                if banner == 2:
                    # drugi banner
                    im = img_usl.crop((szer - 597, 0, szer - 305, wys))
                    im.save(f'img/{f.nr_banera}.png','png')
                    print(f'baner - {f.nr_banera} - jest')
                if banner == 3:
                    # trzeci banner
                    im = img_usl.crop((szer - 292, 0, szer, wys))
                    im.save(f'img/{f.nr_banera}.png','png')
                    print(f'baner - {f.nr_banera} - jest')
        except:
            f.dodaj_rekord('error')

    f.os.remove('img/top_hit_usl.png')
except:
    print('\nError')
#---------------------------------------------------------------------------------------
#--------------------------hity dnia II-------------------------------------------------
#---------------------------------------------------------------------------------------
hity2_bannery = kod_zrodlowy.find(id='day-deals-section')

#tytul sekcji
tytul_sekcji = hity2_bannery.find('h3').get_text().strip()
f.dodaj_rekord(tytul_sekcji)
print('\n' + tytul_sekcji)

#bannery
bannery = hity2_bannery.find_all(class_='day-deal-box')
for ban in range(0,len(bannery)):
    banner = bannery[ban].find(class_='item-content')
    adres = f.dodaj_https(banner.find('a')['href'])
    tytul = banner.find('a').get_text().strip()
    pod_tytul = banner.find(class_='introduction').get_text().strip()
    f.dodaj_rekord(tytul,adres,2,pod_tytul)
    f.pobierz_info_promo_euro(adres)

    adres_img = 'http:' + bannery[ban].find(class_='photo').find('img')['data-original']
    roz_img = f.rozszerzenie_img(adres_img)
    f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
    if roz_img != 'png':
        f.konwertuj_do_png(f.nr_banera,roz_img)

    print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------strefa okazji------------------------------------------------
#---------------------------------------------------------------------------------------
strefa_okazji_bannery = kod_zrodlowy.find(id='opportunity-zone-section')

#tytul sekcji
tytul_sekcji = strefa_okazji_bannery.find(class_='section-header').find(class_='section-title').get_text().strip()
f.dodaj_rekord(tytul_sekcji)
print('\n' + tytul_sekcji)
#bannery
bannery = strefa_okazji_bannery.find(class_='section-container')
#bannery rotacyjne
bannery_rotacyjne = bannery.find(id='opportunity-zone-carousel').find_all(class_='opportunity-item')
#bannery mniejsze
bannery_mniejsze = bannery.find(class_='opportunity-zone-small').find_all(class_='opportunity-box')
for sekcja in (bannery_rotacyjne,bannery_mniejsze):
    for ban in range(0,len(sekcja)):
        banner = sekcja[ban].find(class_='item-content')
        adres = f.dodaj_https(banner.find('a')['href'])
        tytul = banner.find('a').get_text().strip()
        pod_tytul = banner.find(class_='introduction').get_text().strip()
        if sekcja == bannery_rotacyjne:
            f.dodaj_rekord(tytul,adres,1,pod_tytul)
            f.pobierz_info_promo_euro(adres)
        else:
            f.dodaj_rekord(tytul,adres,2,pod_tytul)
            f.pobierz_info_promo_euro(adres)
        
        adres_img = 'http:' + sekcja[ban].find(class_='photo').find('img')['data-original']
        roz_img = f.rozszerzenie_img(adres_img)
        f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
        if roz_img != 'png':
            f.konwertuj_do_png(f.nr_banera,roz_img)

        print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------wszystko co nowe---------------------------------------------
#---------------------------------------------------------------------------------------
wszystko_co_nowe_bannery = kod_zrodlowy.find(id='new-deals-section')

tytul_sekcji = wszystko_co_nowe_bannery.find('h3').get_text().strip()
f.dodaj_rekord(tytul_sekcji)
print('\n' + tytul_sekcji)

bannery = wszystko_co_nowe_bannery.find(class_='new-deal-boxes').find_all(class_='new-deal-box')
for ban in range(0,len(bannery)):
    banner = bannery[ban].find(class_='item-content')
    adres = f.dodaj_https(banner.find('a')['href'])
    tytul = banner.find('a').get_text().strip()
    pod_tytul = banner.find(class_='introduction').get_text().strip()
    f.dodaj_rekord(tytul,adres,2,pod_tytul)
    f.pobierz_info_promo_euro(adres)

    adres_img = 'http:' + bannery[ban].find(class_='photo').find('img')['data-original']
    roz_img = f.rozszerzenie_img(adres_img)
    f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
    if roz_img != 'png':
        f.konwertuj_do_png(f.nr_banera,roz_img)
    
    print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------promocje tygodnia--------------------------------------------
#---------------------------------------------------------------------------------------
promocje_tygodnia = kod_zrodlowy.find(id='weekly-promotions-section')

tytul_sekcji = promocje_tygodnia.find('h3').get_text().strip()
f.dodaj_rekord(tytul_sekcji)
print('\n' + tytul_sekcji)

bannery = promocje_tygodnia.find(id='weekly-promotions-carousel').find_all(class_='promotion-item')
for ban in range(0,len(bannery)):
    banner = bannery[ban].find(class_='promotion-item-box')
    adres = f.dodaj_https(banner.find(class_='promotion-heading').find('a')['href'])
    tytul = banner.find(class_='promotion-heading').find('a').get_text().strip()
    pod_tytul = banner.find(class_='introduction').get_text().strip()
    f.dodaj_rekord(tytul,adres,2,pod_tytul)
    f.pobierz_info_promo_euro(adres)

    adres_img = 'http:' + bannery[ban].find(class_='photo').find('img')['data-original']
    roz_img = f.rozszerzenie_img(adres_img)
    f.zapisz_grafike(adres_img,roz_img,f.nr_banera)
    if roz_img != 'png':
        f.konwertuj_do_png(f.nr_banera,roz_img)

    print(f'baner - {f.nr_banera} - jest')

#---------------------------------------------------------------------------------------
#--------------------------stopka-------------------------------------------------------
#---------------------------------------------------------------------------------------
stopka_sekcja = kod_zrodlowy.find(id='main-footer')
bannery = stopka_sekcja.find(class_='section-services').find_all(class_='service-element')

okno.set_window_size(1600,wys_stopka)
f.time.sleep(5)

okno.execute_script(f"window.scrollTo(0, {wys_top + wys_main + 57});")
okno.save_screenshot('img/stopka.png')

img = f.Image.open('img/stopka.png')
szer, wys = img.size
im = img.crop((185,wys_top + wys_top_menu + 165,szer - 198,wys_top + wys_top_menu + 245))
im.save('img/stopka.png','png')
img = f.Image.open('img/stopka.png')
szer, wys = img.size

print('\nStopka')

for ban in range(0,len(bannery)):
    tytul = bannery[ban].find(class_='info').get_text().strip()
    adres = f.dodaj_https(bannery[ban].find(class_='info').find('a')['href'])
    f.dodaj_rekord(tytul,adres)

    if ban == 0:
        # banner 1
        im = img.crop((0,0,230,wys))
        im.save(f'img/{f.nr_banera}.png','png')
    if ban == 1:
        # banner 2
        im = img.crop((305,0,560,wys))
        im.save(f'img/{f.nr_banera}.png','png')
    if ban == 2:
        # banner 3
        im = img.crop((605,0,900,wys))
        im.save(f'img/{f.nr_banera}.png','png')
    if ban == 3:
        # banner 4
        im = img.crop((920,0,1190,wys))
        im.save(f'img/{f.nr_banera}.png','png')

    print(f'baner - {f.nr_banera} - jest')

f.os.remove('img/stopka.png')
okno.close()
#---------------------------------------------------------------------------------------
f.zapisz_dane_do_docx('euro')