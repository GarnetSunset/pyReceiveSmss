import phonenumbers
import requests
import re
import sys
from bs4 import BeautifulSoup

def getPhoneNum(region):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    }

    session = requests.Session()
    response = session.get('https://receive-smss.com/', headers=headers)

    soup = BeautifulSoup(response.content, 'lxml')

    numbers = soup.findAll('h4', attrs={'class':'number-boxes-itemm-number'})
    regions = soup.findAll('h5', attrs={'class':'number-boxes-item-country number-boxess-item-country'})
    registerStatus = soup.findAll('a', attrs={'class':'number-boxes-item-button number-boxess-item-button button blue stroke rounded tssb'})

    numberofnumbers = len(numbers)
    count = 0 
    choose = 1
    selectionCounter = {}
    countrycode = 0

    if region != "":
        while int(region) != int(countrycode):
            if registerStatus[count].text != "Registered Users":
                parseMe = phonenumbers.parse(numbers[count].text, None)
                countrycode = parseMe.country_code
                selection = str(re.findall('\d+', numbers[count].text)[0])
            count += 1
        print("Selected Number is: " + str(selection))
    else:
        while count != numberofnumbers:
            if registerStatus[count].text != "Registered Users":
                parseMe = phonenumbers.parse(numbers[count].text, None)
                numberOnly = re.findall('\d+', numbers[count].text )
                selectionCounter[choose] = numberOnly
                print(str(choose) + ". " + str(parseMe))
                choose += 1
            count += 1
            
        print("Choose your phone number to send to:")
        whichOne = input("Which entry should we receive texts from? Type the number in the list.:\n")
        selection = str(selectionCounter.get(int(whichOne))[0])
    return selection

def getTexts(phoneNumber):

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:76.0) Gecko/20100101 Firefox/76.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
    }

    session = requests.Session()
    
    response = session.get('https://receive-smss.com/sms/'+phoneNumber, headers=headers)
    
    copyPart = ""
    count = 1
    results = {}
    
    soup = BeautifulSoup(response.content, 'lxml')
    messages = soup.findAll('tr')
    for message in reversed(messages):
        getStuff = []
        children = message.findChildren("td" , recursive=True)
        for child in children:
            getStuff.append(child.text)
            clipboard = child.findAll('b')
            for copy in clipboard:
                if copyPart != "":
                    copyPart = copyPart + "-"
                copyPart = copyPart + copy.text
        if len(getStuff) == 7:
            result = [str(getStuff[1]),str(getStuff[4]),str(getStuff[5]),str(copyPart)]
            copyPart = ""
            results[count] = result
            count += 1
    return results
            
if __name__ == '__main__':
    if len(sys.argv) > 1:
        if len(sys.argv[1]) < 4:
            phoneNumber = getPhoneNum(sys.argv[1])
            print(getTexts(phoneNumber))
        else:
            print(getTexts(sys.argv[1]))
    else:
        phoneNumber = getPhoneNum("")
        print(getTexts(phoneNumber))
