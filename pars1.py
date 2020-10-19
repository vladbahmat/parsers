import requests
from bs4 import BeautifulSoup
import json

url="https://www.mebelshara.ru/contacts"
r=requests.get(url)
soup=BeautifulSoup(r.text,'lxml')
shop_list=soup.find_all('div',{'class':'city-item'})
f=open('pars1.json', 'w')
f.write("[")
for elem in shop_list:
    city=elem.find('h4',{'class':'js-city-name'}).text
    address=elem.find_all('div',{'class':'shop-address'})
    shop_name=elem.find_all('div',{'class':'shop-name'})
    shop_phone=elem.find_all('div',{'class':'shop-phone'})
    shop_weekends=elem.find_all('div',{'class':'shop-weekends'})
    shop_work_time=elem.find_all('div',{'class':'shop-work-time'})
    test_list=elem.find_all('div',{'class':'shop-list-item'})
    count=0
    for name in test_list:
        name=str(name)
        check1=name.find('data-shop-longitude')
        check2=name.find('data-shop-latitude')
        temp=city+','+address[count].text
        arr=[float(name[(check1+21):name.find('"',(name.find('data-shop-longitude')+21))]),float(name[(check2+20):name.find('"',(name.find('data-shop-latitude')+20))])]
        time=[shop_weekends[count].text,shop_work_time[count].text]
        phones=[shop_phone[count].text]
        x={
            "adress":temp,
            "latlon":arr,
            "name":str(shop_name[count].text),
            "phones":phones,
            "working_hours": time,
        }
        with open('pars1.json', 'a') as f:
            f.write(json.dumps(x,ensure_ascii=False))
            f.write(',\n')
        count+=1
f=open('pars1.json', 'a')
f.write("]")
#print(shop_list)
