import requests
from bs4 import BeautifulSoup
import os.path

#grab url and soup it up
url ='https://kenpom.com/index.php?y=2019'
r = requests.get(url).text
soup = BeautifulSoup(r, 'lxml')

#set file name and write headers
path = 'C:\\Users\\user_name\\Desktop'
filename = 'kp_scrape_losses.csv'
complete_name = os.path.join(path, filename)
f = open(complete_name,'w')
headers = 'AdjEM, Best, # of losses, Worst, AdjEM \n'
f.write(headers)

#get all team data rows
table = soup.find('table',{'id':'ratings-table'}).tbody
[tr.extract() for tr in table.find_all('tr',class_=["thead1","thead2"])]
teams = table.find_all('tr')

#get a list of all loss totals
l_list = []
for team in teams:
    rows = team.findAll('td')
    record = (rows[3].text)
    w,l = record.split('-')
    l = int(l)
    l_list.append(l)
count = max(l_list)
min_losses = min(l_list)
#write out data
for x in range(min_losses,count+1):
    #find max_AdjEM
    max_AdjEM = -100
    min_AdjEM = 100
    for team in teams:
        name = team.find('td',{'class':'next_left'}).a.text
        rows = team.findAll('td')
        AdjEM = rows[4].text
        AdjEM = float(AdjEM)
        record = (rows[3].text)
        w,l = record.split('-')
        l = int(l)
        if l == x:
            if AdjEM > max_AdjEM:
                max_AdjEM = AdjEM
                max_name = name
    #find min_AdjEM
    for team in teams:
        name = team.find('td',{'class':'next_left'}).a.text
        rows = team.findAll('td')
        AdjEM = rows[4].text
        AdjEM = float(AdjEM)
        record = (rows[3].text)
        w,l = record.split('-')
        l = int(l)
        if l == x:
            if AdjEM < min_AdjEM:
                min_AdjEM = AdjEM
                min_name = name
    f.write(str(max_AdjEM) + "," + max_name + "," + 
            str(x) + "," + min_name + "," + str(min_AdjEM) + '\n')
          
f.close()
