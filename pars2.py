import requests
from bs4 import BeautifulSoup
import json

def worktime_check(hours):
    timetable=''
    timetable_list=[]
    workdays=hours['workdays']
    saturday=hours['saturday']
    sunday=hours['sunday']
    if workdays['isDayOff']:
        timetable+=' пн-пт Выходной '
    else:
        timetable=timetable+'пн-пт '+workdays['startStr']+' до '+workdays['endStr']
    timetable_list.append(timetable)
    timetable=' '
    if saturday['isDayOff']:
        timetable+=' суббота выходной '
    else:
        timetable=timetable+' суббота '+workdays['startStr']+' до '+workdays['endStr']
    timetable_list.append(timetable)
    timetable=' '
    if sunday['isDayOff']:
        timetable+=' воскресенье Выходной '
    else:
        timetable=timetable+' воскресенье '+workdays['startStr']+' до '+workdays['endStr']
    timetable_list.append(timetable)
    return timetable_list

f=open('pars2.json', 'w')
f.write("[")
for count in range(2000,2523):
    url="https://apigate.tui.ru/api/office/{}".format(count)
    r=requests.get(url)
    soup=BeautifulSoup(r.text,'lxml')
    temp=soup.find('p').text
    data=json.loads(temp)
    try:
        simple=data['office']
        latlon=[simple['latitude'],simple['longitude']]
        address=simple['address']
        name=simple['name']
        phones=simple['phones']
        phone_list=[]
        for elem in phones:
            phone_list.append(elem['phone'])
        hours1=simple['hoursOfOperation']
        x={
            "adress":address,
            "latlon":latlon,
            "name":name,
            "phones":phone_list,
            "working_hours": worktime_check(hours1),
        }
        with open('pars2.json', 'a') as f:
            f.write(json.dumps(x,ensure_ascii=False))
            f.write(',\n')
    except:
        pass
f=open('pars2.json', 'a')
f.write("]")

