#URL QA automation

#Step 1: -Importing the Necessary Libraries
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import numpy as np

try:
    #Step 2: - Taking input the of refrence file(So called URL Matrix) as input
    CIMS_ID = input("Enter the CIMS of the Campaign: ")
    PID_ID = input("Enter the PID of the Campaign: ")
    market = input("Enter the Market of the Campaign: ")
    file_name = "URL_QA_Result_CIMS"+CIMS_ID+"_PID"+PID_ID+"_"+market+".csv"
    link_ViewAsWebPage = Request(input("Enter the View as webpage link For the Email You want To do QA: "))
    excl_URLMatrix = input("Enter the path of URL Matrix from your Local Drive: ")


    #Step 2: - Extracting the links from Email: - Using View as WebPage Link of Email we will try to extract the URL(direct link not forward links) from the Email. Along with that We are having one more coloumn for status bit i.e. incae the URL passed is a good URL or BAD. Good URL: - Any Request status between 200 to 399. Bad URL: - Any Request status between 400 to 599.
    html = urlopen(link_ViewAsWebPage) # Insert your URL to extract
    bsObj = BeautifulSoup(html.read(features="lxmx"));
    lst_URLOfQA =[]
    lst_Status = [] 
    for link in bsObj.find_all('a'):
        link_redirect = link.get('href')
        #print(link_redirect)
        data = requests.request("GET", link_redirect)
        link_direct = data.url
        #link_status = link_direct.getcode()
        time.sleep(1)
        #lst_Status.append(link_status)
        lst_URLOfQA.append(link_direct)
    #print(link_Status)
    #temp_url = urlopen(Request(link.get('href')))
    #print(temp_url)
    #lst_URLOfQA.append(Request(link.get('href')))
    lst_URLOfQA = lst_URLOfQA[1:]
    #Step 4: -Once got the URL Matrix we will Use "Placement" and "Full URL" Couloum for comparistion
    data_URLMatrix = pd.read_excel(excl_URLMatrix)
    df_URLMatrix = pd.DataFrame(data_URLMatrix)
    lst_FullURL = list(df_URLMatrix["Full URL"])
    lst_Comparision = [True if lst_FullURL[i] == lst_URLOfQA[i] else False  for i in range(len(lst_FullURL))]
    df_ResultURL = pd.concat([df_URLMatrix,pd.DataFrame(lst_URLOfQA),pd.DataFrame(lst_Status),pd.DataFrame(lst_Comparision)], axis=1, ignore_index=True, keys = ["Placement", "Orignal URL", "Email URL", "Status of URL", "Comparision"])
    df_ResultURL.columns = ["Placements", "Full URL", "Destination URL", "Comparision"]
    df_ResultURL.to_csv(file_name, sep='^', encoding='utf-8', index=False)

except Exception as e:
    print(e)


