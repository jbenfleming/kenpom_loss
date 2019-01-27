import requests
from bs4 import BeautifulSoup
import os.path

#grab url and soup it up
url ='https://kenpom.com/index.php?y=2019'
r = requests.get(url).text
soup = BeautifulSoup(r, 'lxml')

#set file name and write headers
path = 'C:\\Users\\username\\Desktop'
filename = 'kp_scrape_wl.csv'
complete_name = os.path.join(path, filename)
f = open(complete_name,'w')
headers = 'Rank, AdjEM, Best, # of losses, Worst, Rank, AdjEM, , Diff \n'
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
    max_check = False
    min_check = False
    
    #find max_AdjEM
    max_AdjEM = -100
    min_AdjEM = 100
    for team in teams:
        name = team.find('td',{'class':'next_left'}).a.text
        rows = team.findAll('td')
        AdjEM = rows[4].text
        AdjEM = float(AdjEM)
        rank = rows[0].text
        record = (rows[3].text)
        w,l = record.split('-')
        l = int(l)
        if l == x:
            if AdjEM > max_AdjEM:
                max_AdjEM = AdjEM
                max_name = name
                max_rank = rank
                max_check = True
               
    #find min_AdjEM
    for team in teams:
        name = team.find('td',{'class':'next_left'}).a.text
        rows = team.findAll('td')
        AdjEM = rows[4].text
        rank = rows[0].text
        AdjEM = float(AdjEM)
        record = (rows[3].text)
        w,l = record.split('-')
        l = int(l)
        if l == x:
            if AdjEM < min_AdjEM:
                min_AdjEM = AdjEM
                min_name = name
                min_rank = rank
                min_check = True
     
    diff = abs(max_AdjEM - min_AdjEM)
                      
    #check to find mising loss numbers
    if not max_check:
        max_AdjEM = ' '
        max_name = ' '
    if not min_check:
        min_AdjEM = ' '
        max_name = ' '
     
    #write values to csv
    f.write(str(max_rank) + "," + str(max_AdjEM) + "," + max_name + "," + 
            str(x) + "," + min_name + "," + str(min_rank) + "," + 
            str(min_AdjEM) + "," + " " + "," + str(diff) + '\n')
          
f.close()
