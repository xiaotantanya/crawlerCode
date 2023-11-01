import requests
import time
from bs4 import BeautifulSoup
import logging
import pickle
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
def printTime(func,paraDict):
    start_time = time.time()
    result = func(paraDict)
    end_time = time.time()
    logging.warning("time elapsed: {}".format(end_time-start_time))
    return result

def getUrlList(paraDict):
    baseUrl = paraDict["baseUrl"]
    # logging.info(baseUrl)
    res = requests.get(baseUrl)
    res.encoding = 'utf-8'
    urlList = []
    soup = BeautifulSoup(res.text,features='html.parser')
    
    liItems = soup.findAll("li")
    aItems = []
    for li in liItems:
        if li is not None:
            aItems.append(li.find("a"))
    
    # logging.info(aItems)
    for a in aItems:
        if a is not None:
            link = a.get('href')
            if link is not None:
                if 'repository-otc-data' in link:
                    urlList.append(link)
    
    return urlList

def getTableItems(paraDict):
    baseUrl = paraDict["baseUrl"]
    urlList = paraDict["urlList"]
    tableItems = []
    for url in urlList:
        # logging.info(baseUrl+url)
        if 'https' in url:
            res = requests.get(url)
        else:
            res = requests.get(baseUrl+url)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text,features='html.parser')
        tableItem = soup.find("div",class_="mobileWindow")
        if tableItems is None:
            logging.info(f"{url} result is None")
        tableItems.append(tableItem)
    return tableItems


if __name__ == '__main__':
    paraDict={"baseUrl":"https://www.dtcc.com/repository-otc-data#Top1000"}
    result = printTime(getUrlList,paraDict)
    result = result[1:]
    logging.info(result)
    logging.info(len(result))
    paraDict["baseUrl"] = "https://www.dtcc.com"
    paraDict["urlList"] = result
    tableItems = printTime(getTableItems,paraDict)
    logging.info(tableItems)
    # with open('tableItems.pickle','wb') as file:
    #     pickle.dump(tableItems,file)
    
    
    
    