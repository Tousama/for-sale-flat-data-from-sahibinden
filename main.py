import requests
from bs4 import BeautifulSoup
import time
import constants

URL = constants.url
HEADERS = constants.headers
CITIES = constants.cities
payload = []

for i in range(len(CITIES)):
    payload.append({"pages": CITIES[i]})


new_data_list = []

time.sleep(2)
#######################################################################
#   Istanbul bolgesindeki ilanlarin 50 sayfasinin verisinin cekilmesi
#######################################################################
for page in range(50):
    data = []
    if page == 0:
        new_url = URL + "/" + payload[0]["pages"]
    else:
        new_url = URL + "/" + payload[0]["pages"] + "?pagingOffset=" + str(page * 20)
    r = requests.get(new_url, headers=HEADERS)
    print(f"Status code: {r.status_code}")
    soup = BeautifulSoup(r.text, 'html.parser')
    d = soup.find("div", {"class": "searchResultsPage uiContent"}).find("table",{"id":"searchResultsTable"}).find("tbody", {"class":"searchResultsRowClass"})
    for i in d:
        if i == "\n":
            pass
        else:
            data.append(i.text)

    #################################################################
    #   Elde edilen verilerin {title, area, number of rooms, price...}
    #   gibi kategorilere  ayrılarak listelenmesi
    #################################################################

    def extract_data(index):
        global i
        data_dict = {}
        data[index] = data[index].replace("\n", "").split("  ")
        for i in range(len(data[index]) - 1, -1, -1):
            if data[index][i] == "":
                data[index].pop(i)
        try:
            data_dict["title"]=data[index][0]
            data_dict["area"]=data[index][1]
            new_data = data[index][2].split(" ")
            data_dict["numberOfRooms"]=new_data[0]
            data_dict["price"]=new_data[1]
            for i in range(1, len(data[index][-1])):
                if data[index][-1][i]==data[index][-1][i].upper():
                    data_dict["town"]=data[index][-1][:i]
                    data_dict["district"]=data[index][-1][i:]
            new_data_list.append(data_dict)
        except:
            pass


    #Her sayfadaki verileri elde etmek icin sayfadaki ilan sayisi kadar extract_data metodu cagrilir.
    for i in range(len(data)):
        extract_data(i)

    ###########################################################################
    #   Sayfalara request yaptigimizda Error 429 (Cok fazla request sonucu ban)
    #   yememek icin 45 saniyelik ara vermek
    ###########################################################################
    time.sleep(50)

print(new_data_list)