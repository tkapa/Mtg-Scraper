#Scrapping shit
from bs4 import BeautifulSoup
from urllib import request
from requests import get
import requests

#Random
import json

global output
output = []

global existingData
existingData = []


def GetCards():
    url = "http://magiccards.info/akh/en.html"
    h = {'User-Agent': 'Chrome'}
    req = request.Request(url, headers=h)
    data = request.urlopen(req)
    soup = BeautifulSoup(data, 'html.parser')
 
    tableEven = soup.find_all('tr', {'class': 'even'})
    tableOdd = soup.find_all('tr', {'class': 'odd'})

    cardTable = tableEven + tableOdd
    
    for row1 in cardTable:
        cardUrl = "http://magiccards.info" + row1.find_all('td')[1].a['href']
        cardImgUrl = "http://magiccards.info/scans" + row1.find_all('td')[1].a['href']
        cardName = row1.find('a').text
        cardType = row1.find_all('td')[2].text        
        if row1.find_all('td')[3].text is "":
            cardMana = 'None'
        else:
            cardMana = row1.find_all('td')[3].text
        cardRarity = row1.find_all('td')[4].text
        cardDescription = GetCardDescription(cardUrl)
        cardFlavour = GetCardFlavour(cardUrl)
        cardArtist = row1.find_all("td")[5].text

        output.append({"Name": cardName, "Mana Cost": cardMana, "Rarity": cardRarity, "Type": cardType, "Artist": cardArtist, "Flavour Text": cardFlavour, "Image URL": cardImgUrl, "Description": cardDescription})
        
        print("Got card " + cardName)


def GetCardDescription(card_url):
    h = {'User-Agent': 'Chrome'}
    source_code = request.Request(card_url, headers=h)
    d_ = request.urlopen(source_code)
    soup = BeautifulSoup(d_, 'html.parser')

    if soup.find('p', {'class': 'ctext'}).b.text is "":
        desc = "None"
    else:
        desc = soup.find('p', {'class': 'ctext'}).b.text
    
    return desc


def GetCardFlavour(card_url):
    h = {'User-Agent': 'Chrome'}
    source_code = request.Request(card_url, headers=h)
    d_ = request.urlopen(source_code)
    soup = BeautifulSoup(d_, 'html.parser')
    
    cardImg = soup.findAll('p')[2].text

    return cardImg


def StoreCards():
        
    file = open("MTGAPI.json", "w")
    output.append(existingData)
    json.dump(output, file, indent=4, sort_keys=True)
    print('Parsed out output')
    file.close()

def main():
    GetCards()
    StoreCards()


if __name__ == "__main__":
    main()
