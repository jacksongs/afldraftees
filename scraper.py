# This scraper collects all the AFL draftees from the FootyWire website

import scraperwiki
import requests
from bs4 import BeautifulSoup

years = ['2010','2011','2012','2013','2014']
drafts = ['National','Pre-season','Rookie','Mini-draft']

players = []
for y in years:
    for d in drafts:
        fw = requests.get("http://www.footywire.com/afl/footy/ft_drafts?year=%s&t=%s&s=P"%(y,d[0]))
        fwsoup = BeautifulSoup(fw.content)
        table = fwsoup.find("table",attrs={"width":588})
        trfirst = table.find("tr")
        tds = trfirst.find_all("td")
        cats = []
        for td in tds:
            if td.text == u'\xa0':
                cats.append('Notes')
            else:
                cats.append(td.text)
        trs = table.find_all("tr")
        for i,tr in enumerate(trs):
            tds = tr.find_all("td")
            if i>0:
                player = {'Draft year': y, 'Draft': d}
                for i,td in enumerate(tds):
                    player[cats[i]] = td.text.strip()
                players.append(player)



scraperwiki.sqlite.save(unique_keys=["Player","Draft year","Pick"], data=players, table_name='draftees')
