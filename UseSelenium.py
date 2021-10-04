# -*- coding: utf-8 -*-
"""
Created on Fri Sep 17 21:42:09 2021

@author: BektasBaysal
"""
from selenium import webdriver #Bir tarayıcıyı başlatmanıza izin verir
from selenium.webdriver.common.by import By  #Belirli parametreleri kullanarak şeyler aramanıza izin verir
from selenium.webdriver.support.ui import WebDriverWait # açılan tarayıcada kalmamızı sağlar
from selenium.webdriver.support import expected_conditions as EC # belirli bir koşulun oluşmasını beklemek için tanımlanan bir koddur
from selenium.webdriver.chrome.options import Options # Tarayıcı ayarlarını yapmak için kullanılır
from datetime import datetime
import time
import json

driver_path = "chromedriver.exe"
ayarlar = Options()
ayarlar.add_argument("--headless")  #tarayıcıyı açmadan veri çekmeyi sağlar 
browser = webdriver.Chrome(executable_path=driver_path,options=ayarlar)     
timeout = 10
vatanLink = 'https://www.vatanbilgisayar.com/cep-telefonu-modelleri/'
mediaMarketLink = 'https://www.mediamarkt.com.tr/tr/category/_android-telefonlar-675172.html'

def VatanScraping(browserLink, timeout):
    data = []
    condition = True
    browser.get(browserLink)
    while condition:
        
        elements = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='product-list product-list--list-page']//div[@class='product-list__content']//a[@class='product-list__link']")))
        
        for element in elements:
            
            href = element.get_attribute('href')
            
            #href için yeni sekme açma
            browser.execute_script("window.open('" +href +"');")
            # yeni sekme geçme
            browser.switch_to.window(browser.window_handles[1])
            
            isim = WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.CLASS_NAME, "product-list__product-name")))
            # print(isim.text)       
            
            fiyat = WebDriverWait(browser, timeout).until(EC.visibility_of_element_located((By.XPATH, "//div[@class='product-list__cost product-list__description']//span[@class='product-list__price']")))
            # print(fiyat.text)
            
            data.append({
                "product_name": isim.text,
                "product_price": fiyat.text
                })
            with open('vatan.json', 'w', encoding='utf8') as outfile:
                json.dump(data, outfile,ensure_ascii=False)
            #sekme kapatma
            browser.close()
            #ilk sekmeye geri dönme
            browser.switch_to.window(browser.window_handles[0])
        try:
            browser.find_element_by_class_name('pagination__item').find_element_by_tag_name('a').get_property('href')
            browser.find_element_by_class_name('icon-angle-right').click()
            
        except:
            condition= False
    print("VatanBilgisayar Bitti")
    # browser.quit()
    return data


def MMScraping(browserLink,timeout):
    
    browser.get(browserLink)
    condition= True  
    linkler = []
    fiyatlar = []
    IDlist = []
    data = []
    
    while condition:
        elements = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='content ']//h2//a")))
        for element in elements:
            href = element.get_attribute('href')
            linkler.append(href)
            browser.execute_script("window.open('" +href +"');")
            browser.switch_to.window(browser.window_handles[1])            
            
            time.sleep(1)
            ###### isim kazıma
            """isimler tamamdır"""
            name = browser.find_element_by_class_name('details').find_element_by_tag_name("h1")
            # print(name.text)
               
            """fiyatlar çekildi"""
            priceValue = browser.find_element_by_xpath("//meta[@itemprop='price']")
            price = priceValue.get_attribute("content")
            fiyatlar.append(price)
            # print(price )
            
            """id"""
            try:
                ProductId = browser.find_element_by_xpath("//span[@itemprop='sku']")
                _, ProductID = ProductId.get_attribute("content").split(':')
                IDlist.append(ProductID)
                # print(ProductID)
            except:
                ProductID = 'ID Empty'
                IDlist.append(ProductID)
                pass

            data.append({
                "product_name": name.text,
                "product_id": ProductID,
                "product_price": price
                })

            with open('mediamarket.json', 'w', encoding='utf8') as outfile:
                json.dump(data, outfile,ensure_ascii=False)
                
            browser.close()
            browser.switch_to.window(browser.window_handles[0])     


        try:            
            PageHref = WebDriverWait(browser, timeout).until(EC.visibility_of_all_elements_located((By.XPATH, "//li[@class='pagination-next']//a")))
            for PageElemen in PageHref:
                pagehref = PageElemen.get_attribute('href')
                # print(pagehref)
                browser.get(pagehref)            
        except :
              condition = False 
    print("MediaMarket Bitti")     
    # browser.quit()
    return data 



start = datetime.now()
ResultVatan = VatanScraping(vatanLink, timeout)
time.sleep(2)
ResultMM = MMScraping(mediaMarketLink, timeout) 
browser.quit()           
end = datetime.now()
print(end-start)