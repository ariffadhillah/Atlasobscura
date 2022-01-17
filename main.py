from email.headerregistry import Address
import requests
from bs4 import BeautifulSoup


import pandas as pd

baseurl = 'https://www.atlasobscura.com'

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0'
}

productLink = []
for x in range(1,600):
    res = requests.get(f'https://www.atlasobscura.com/things-to-do/united-states/places?page={x}', headers=headers)
    soup = BeautifulSoup(res.content, 'lxml')

    productList = soup.find_all('div', class_='index-card-wrap')
        # print(productList)


    for item in productList:
        for link in item.find_all('a', href=True):
                # print(link['href'])
            productLink.append(baseurl + link['href'])

# print(productLink)\
AtlasobscuraList = []

for link in productLink:

    res = requests.get(link, headers=headers)
    soup = BeautifulSoup(res.content, 'lxml')
    
    name = soup.find('h1', class_='DDPage__header-title').text.strip()
    city = soup.find('div', class_='DDPage__header-place-location').text.strip()
    discription = soup.find('h3', class_='DDPage__header-dek').text.strip()
    LatitudeLongitude = soup.find('div', class_='DDPageSiderail__coordinates js-copy-coordinates').text.strip()
    try:
        OpenOrClose = soup.find('div', class_='place-closed-banner').text.strip()
    except:
        OpenOrClose = 'Open'

    
    
    atlasobscura = {
        # 'link': productList,
        'name': name,
        'City State' : city,
        'Description' : discription,
        'Latitude Longitude' : LatitudeLongitude,
        'Open or Closed': OpenOrClose,
    }
    AtlasobscuraList.append(atlasobscura)
    print('Saving' , atlasobscura['name'])


df =pd.DataFrame(AtlasobscuraList)
print(df.head)
df.to_csv('Atlasobscura.csv', encoding='utf-8')




