import requests
import re

file = open("Longlist.csv")
# this is the html tag to identify the knowledge panel in the page
html_tags = {
    'knowledge_panel': 'kp-blk knowledge-panel Wnoohf OJXvsb',
}
# headers
headers_Get = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

#creates the get request url
def queryCreator(query):# creates the url for the search
    s = requests.Session()
    query = query.replace(" & ", "&", 10)  # this changes
    query = query.replace("&", " %26 ",
                          10)  # this changes & signs into browers equivilent so the url can handle the and signs correctly.
    query = query.replace(",", " ", 10)
    query = '+'.join(query.split())
    # print("this is the query",query)
    createdUrl = 'https://www.google.com/search?q=' + query + '&ie=utf-8&oe=utf-8'
    # print(createdUrl)
    return createdUrl


def get_Value(string, tag, regex, distance):# this will be our function for getting each n value that is given
    if (tag not in string):
        print("returning")
        return None
    index = string.find(tag)  # this gets the actual location of the character of the phone number in the website code
    substr = string[index:index + distance]  # this gets the sub string where the phone number will be
    if re.search(regex, substr):  # search in between the given tags with a greed for any number of characters

        return re.search(regex, substr).group(1)  # return the phone number
    else:
        return None


def export(data):  # export the name of the buissiness its location etc with the phone number
    cleanfile = open("clean phone number spread sheet", "w")
    cleanfile.write("fill this in ")


def fileWriter(line):  # pass in a value to add to the spreadsheet line
    newfile = open("new spreadsheet.csv", "a")
    line = line.replace("\n", "", 10)
    newfile.write(line + "\n")
    newfile.close()


# print("hit")
def lineMaker(Value, line):
    line = line + Value + ","
    return line
def dataManager(request,line):
        PhoneRegex = "<span>(.*?)</span>"  # this finds any number of characters between span and /span , this is where phone number will be found.
        AddressRegex = '<span class="LrzXr">(.*)</span>'
        # this is predefined and can be checked with inspect element
        phoneTags = "LrzXr zdqRlf kno-fv"  # if you inspect element and ctrl f this it will bring you close to the phone number. There are codes for each set of information
        AddressTags = "kc:/location/location:address"  # this is the code for address
        phone_number = get_Value(request.text, phoneTags, PhoneRegex, 200)
        Address = get_Value(request.text, AddressTags, AddressRegex, 1000)
        if (phone_number):
            line = lineMaker(phone_number, line)
        if (Address):
            PostCode = Address[-9:]
            line = lineMaker(PostCode, line)
        return phone_number, Address,line
def normalMain():
    connecting = True
    list = []
    for line in file:  # makes the string that will be googled, cuts out the commas and adds spaces
        # simulating selecting the row in the spreadsheet
        if connecting:
            URL = queryCreator(line)
            request = requests.get(URL, headers =headers_Get)
            print(request)
            print(request.text)
            flag = (html_tags['knowledge_panel'] in request.text)
            if (flag):
                print("flag")
                phone_number,Address,line = dataManager(request,line)
                print(line)
                fileWriter(line)
            elif("captcha" in  request.text):
                print("captcha wall hit, try using proxies, wrting out left overs dont exit")
                connecting = False
                file2 =open("newLonglist.csv","w")
                file2.close()
        else:
            file2 = open("newLonglist.csv","a")
            file2.write(line)
print("finished writing out you may exit ")


def menu():
    ProxyChoice = input(" would you like to use a proxy (Y/N")
    if ProxyChoice == "Y":
       # proxyMain()
       pass
    else:
        normalMain()
menu()
