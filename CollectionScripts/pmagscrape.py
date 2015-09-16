from bs4 import BeautifulSoup
import re
import HTMLParser
import requests
import urllib2
import pandas as pd


#Create empty list for creating pandas dataframe
listentries = []

#Pmag issues 1 through 2299 have different html tags

for issue in range(2299,2473):

        url = "http://www.poetryfoundation.org/poetrymagazine/toc/" + str(issue)

        #Convenience field
        urlnum = issue
        
        #Not every number links to a magazine issue and some will result 404 not found error
        try:
            page = urllib2.urlopen(url)
            soup = BeautifulSoup(page.read())

            issue = re.sub(' : Poetry Magazine', '', soup.title.string)
            
            all_item_tags = soup.find_all('div', class_ = 'item')
            
            #print (issue, len(x))

            #iterate through each item
            for i in range(0,len(all_item_tags)):
                
                poet_info = x[i].find_all('span', class_='author')
                poetname = poet_info[0].get_text()

                #Find all links to poems
                poem_links = x[i].find_all('a', href=re.compile('.*/poem/.*'))
                
                for l in poem_links:

                    poemtitle = l.get_text().encode('ascii','ignore')
                    poemurl = 'http://www.poetryfoundation.org' + l.get('href')
                    poetname = poetname.encode('ascii', 'ignore')
                    issue = re.sub(' : Poetry Magazine', '', issue).encode('ascii', 'ignore')
                    
                    dict1 = {'IssueUrl': urlnum, 'Issue': issue, 'PoetName': poetname, 'PoemTitle': poemtitle, 'PoemUrl': poemurl }
                    
                    listentries.append(dict1)
        except Exception: 
            pass

#Create Pandas DataFrame to contain all the entries from pmag site
pmagdf = pd.DataFrame(listentries)

#For outputting dataframe to excel
writer = pd.ExcelWriter('pmag.xlsx')
pmagdf.to_excel(writer,'Sheet1')
writer.save() 