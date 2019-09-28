import requests
from bs4 import BeautifulSoup
import re
import os
import smtplib
import time
from datetime import datetime

headers = {    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3", 
    "Accept-Encoding": "gzip, deflate", 
    "Accept-Language": "en-US,en;q=0.9", 
    "Host": "stockx.com", 
    "Upgrade-Insecure-Requests": "1", 
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
    }
now = datetime.now()
ultimateList = []
linkList = []
lowestDifference = ["ignoreForNow","0","0","0"]
highestDifference = ["ignoreForNow","0","100","10"]
startTime = now.strftime("%H:%M:%S")
startTimeForCalculations = time.time()
numberOfDuplicates = 0.2
inputList = [
    ["https://stockx.com/sneakers", 25],
    ["https://stockx.com/adidas/iniki", 1], 
    ["https://stockx.com/adidas/iniki", 1], 
    ["https://stockx.com/adidas/stan-smith", 5], 
    ["https://stockx.com/adidas/yeezy", 4], 
    ["https://stockx.com/adidas/eqt", 7], 
    ["https://stockx.com/adidas/nmd", 15],
    ["https://stockx.com/nike/sb", 25], 
    ["https://stockx.com/nike/foamposite", 6],
    ["https://stockx.com/nike/kd", 8],
    ["https://stockx.com/nike/kobe", 12],
    ["https://stockx.com/nike/lebron", 22],
    ["https://stockx.com/nike/air-force", 25],
    ["https://stockx.com/nike/air-max", 25],
    ["https://stockx.com/nike/basketball", 25],
    ["https://stockx.com/nike/footwear", 25],
    ["https://stockx.com/retro-jordans/air-jordan-1", 25],
    ["https://stockx.com/retro-jordans/air-jordan-25", 25],
    ["https://stockx.com/retro-jordans/air-jordan-11", 6],
    ["https://stockx.com/retro-jordans/air-jordan-3", 4],
    ["https://stockx.com/retro-jordans/air-jordan-4", 5],
    ["https://stockx.com/retro-jordans/air-jordan-5", 4],
    ["https://stockx.com/retro-jordans/air-jordan-12", 5],
    ["https://stockx.com/retro-jordans/air-jordan-16", 16],
    ["https://stockx.com/retro-jordans", 25],
    ["https://stockx.com/asics", 16],
    ["https://stockx.com/balenciaga-sneakers", 5],
    ["https://stockx.com/chanel-sneakers", 1],
    ["https://stockx.com/converse", 20],
    ["https://stockx.com/diadora", 5],
    ["https://stockx.com/dior-sneakers", 2],
    ["https://stockx.com/gucci-sneakers", 1],
    ["https://stockx.com/li-ning", 2],
    ["https://stockx.com/louis-vuitton-sneakers", 2],
    ["https://stockx.com/new-balance", 25],
    ["https://stockx.com/other-sneakers", 25],
    ["https://stockx.com/prada-sneakers", 1],
    ["https://stockx.com/puma", 1],
    ["https://stockx.com/reebok", 21],
    ["https://stockx.com/saucony", 8],
    ["https://stockx.com/under-armour", 8],
    ["https://stockx.com/vans", 25]
    ]

def getSizePricesInfo(url):
    output = []
    page = requests.get(url, headers = headers)
    cont = page.content 
    soup = BeautifulSoup(cont,'html.parser')
    soup = str(soup)
    listOfPrices = re.findall(r'"skuUuid":"[\w.-]{0,40}","productUuid":"[\w.-]{0,40}","lowestAsk":(\d{0,6}),"lowestAskSize":"([\w.-]{0,10})","parentLowestAsk":[\w.-]{0,10},"numberOfAsks":[\w.-]{0,10},"salesThisPeriod":[\w.-]{0,10},"salesLastPeriod":[\w.-]{1,10},"highestBid":(\d{1,6})', soup)
    for shoe in listOfPrices:
        output.append([url, shoe[1], shoe[0], shoe[2]])
    return output

def getAllSneakersList(url):
    page = requests.get(url, headers = headers)
    cont = page.content 
    soup = BeautifulSoup(cont,'html.parser')
    soup = str(soup)
    return re.findall(r'"url" : "(https?://stockx.com/[\w.-]{0,50})"', soup)

def addLinksToList(links):
    global linkList
    output = []
    for url in links:
        for i in range(1,(int(url[1])+1)):
            linkList += (getAllSneakersList(str(url[0])+"?page="+str(i)))
        displayStats("Storing links of shoe models. Up Next: Storing price and sizing information about all models")
    return output

def displayStats(status):
    os.system("clear")
    now = datetime.now()
    print("\n\n\n\n\n\n"
    "Status: \t\t\t\t"+status+
    "\nAmount of Models: \t\t\t"+str(len(linkList))+
    "\nAmount of Duplicates Found: \t\t"+str(numberOfDuplicates)+
    "\nTotal amount of Shoes:\t\t\t"+str(len(ultimateList))+
    "\nLowest Difference:\t\t\t"+str(lowestDifference)+
    "\nHighest Difference:\t\t\t"+str(highestDifference)+
    "\nStart Time:\t\t\t\t"+str(startTime)+
    "\nTime of last Update:\t\t\t"+str(now.strftime("%H:%M:%S"))+
    "")

displayStats("Storing links of shoe models. Up Next: Storing price and sizing information about all models")
addLinksToList(inputList)

displayStats("Storing price and sizing information about all models. Up Next: Finding shoes for possible profit")

linkListLength = len(linkList)
linkList = list(dict.fromkeys(linkList))
numberOfDuplicates = linkListLength - len(linkList)
linkListLength = len(linkList)

for link in linkList:
    ultimateList += getSizePricesInfo(link)
    displayStats("Storing price and sizing information about all models. Up Next: Finding shoes for possible profit")

displayStats("Finding shoes for possible profit")

for shoe in ultimateList:
    shoe.append(int(shoe[3]) - int(shoe[2]))

ultimateList = sorted(ultimateList,key=lambda l:l[4], reverse=True)

with open('/Users/21rytel_j/Desktop/stockxfolder/151627.txt', 'w') as filehandle:
    for listitem in ultimateList:
        filehandle.write('%s\n' % listitem)

for shoe in ultimateList:
    # shoe[0] - link
    # shoe[1] - shoe size
    # shoe[2] - buy price
    # shoe[3] - sell price
    if int(shoe[3]) - int(shoe[2]) < int(lowestDifference[3]) - int(lowestDifference[2]):
        lowestDifference = shoe
        displayStats("Finding shoes for possible profit")
    if int(shoe[3]) - int(shoe[2]) > int(highestDifference[3]) - int(highestDifference[2]):
        highestDifference = shoe
        displayStats("Finding shoes for possible profit")
    if int(shoe[3]) - int(shoe[2]) > 0:
        file = open("/Users/21rytel_j/Desktop/SUCCESS.txt","w")
        file.write("Link: "+shoe[0]+" Shoe Size: "+shoe[1]+" Buy Price: "+shoe[2]+" Sell Price: "+shoe[3]+" Profit: "+str(int(shoe[3])-int(shoe[2]))+"\n")
        displayStats("Finding shoes for possible profit")
displayStats("COMPLETED")


#for displayStats add after amount of models (how many pages visited / how many pages to visit)
#for displayStats add after total amount of shoes (how many models visited / how many models total)
