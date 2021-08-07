#
# This file was created by Maple Software
#
#
# This template is usable for TWO-LEVEL DEEP scrapers.
#
#
# HOW IT WORKS:
#
# 1. FOLLOWING: Follow the urls specified in rules.
# 2. SCRAPING: Scrape the fields and populate item.
#
#


from scrapy.loader.processors import MapCompose
from scrapy import Spider
from scrapy import Request
from scrapy.selector import Selector
from w3lib.html import remove_tags
from crawler.loader import MapleLoader
import json


class MySpider(Spider):
    name = 'rentvalley_nl'
    start_urls = ['https://www.rentvalley.nl/nl/realtime-listings/consumer']  # LEVEL 1

    # 1. FOLLOWING
    def parse(self, response):
        
        data = json.loads(response.body)
        
        for item in data:
            follow_url = response.urljoin(item["url"])
            for my_item in item:
                #satır 34 ile beraber içerisinde dolaşılan url ve alt alanlarının 
                #listesinde alan başlıklarına ve onlara karşılık gelen
                #değerlerine  teker teker ulaşmak için for 
                #döngüsünün içinde bir for döngüsü daha kullandım.
                #==>>>item 20 alt kümeden bir tanesi durumunda
                #==>>>my_item içerisine girilen kümenin bir alt alanı durumunda(address,state... gibi) 
                #==>>>item[my_item] ise alanın karşılık değeri(Beukstraat 81 1,None... gibi)
                ###çıktılar stdout'ta veriliyor.
                "*********************************\n**********************************"
                print(f"{my_item}:{item[my_item]}")
                "*********************************\n**********************************"
                #yield item_loader.add_value(my_item,item[my_item])
                #yield item_loader.load_item(my_item,item[my_item])
            
            lat = item["lat"]
            lng = item["lng"]
            yield Request(follow_url, callback=self.populate_item, meta={"lat":lat, "lng":lng})#url
            
        #testing-----------     
        #yield self.paginate(response)
        #testing-----------

    # 2. SCRAPING level 2
    def populate_item(self, response):
        item_loader = MapleLoader(response=response)
        self.logger.info("Visited %s", response.url)#Kovalanan url'ler 
        lat = response.meta.get("lat")#lat değeri için çıktısı True değl
        lng = response.meta.get("lng")#lng değeri için çıktısı True değil
        title = response.xpath("normalize-space(//h1/text())").extract_first()
        item_loader.add_value("title", title)

        
        #item_loader.add_value("lat", lat)
        #item_loader.add_css("","")



        #testing-----
        #item_loader.add_value(self.my_item,self.item[self.my_item])############
        #testing-------
        yield item_loader.load_item()

    
