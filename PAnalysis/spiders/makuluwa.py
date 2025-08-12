import scrapy
import re

from PAnalysis.items import PanalysisItem


class MakuluwaSpider(scrapy.Spider):
    name = "makuluwa"
    allowed_domains = ["www.lankapropertyweb.com"]
    start_urls = ["https://www.lankapropertyweb.com/"]

    def parse(self, response): 
        page_number = 4
        for i in range (1,page_number):
            page_url = f'https://www.lankapropertyweb.com/sale/index.php?page={i}'
            yield scrapy.Request(page_url,callback=self.parse_page)
        pass
    
    def parse_page(self, response):
        item_urls = response.xpath('//article[@class="listing-item"]/a[@class="listing-header"]/@href').getall()
        
        for item_url in item_urls:
            full_link = response.urljoin(item_url)
            yield scrapy.Request(url=full_link,callback=self.parse_item)
             
        pass
    
    def parse_item(self, response):
        price = response.xpath('//span[@class="main_price mb-3 mb-sm-0"]/text()').get()
        price_num = int(re.sub(r"[^\d]", "",price))

        # Extract Property Type
        property_type = response.xpath('//div[@class="overview-item"][div[@class="label mb-2" and contains(text(), "Property Type")]]/div[@class="value"]/text()').get()

        # Extract Bedrooms
        bedrooms = response.xpath('//div[@class="overview-item"][div[@class="label mb-2" and contains(text(), "Bedrooms")]]/div[@class="value"]/text()').get()

        # Extract Bathrooms
        bathrooms = response.xpath('//div[@class="overview-item"][div[@class="label mb-2" and contains(text(), "Bathrooms")]]/div[@class="value"]/text()').get()
        floor_area = response.xpath('//div[@class="overview-item"][div[@class="label mb-2" and contains(text(), "Floor area")]]/div[@class="value"]/text()').get()
        size_num = int(re.sub(r"[^\d]", "", floor_area))
        item = PanalysisItem()
        
        item['price'] = price
        item['property_type'] = property_type
        item['bedrooms'] = bedrooms
        item['bathrooms'] = bathrooms
        item['floor_area'] = floor_area
        item['price_per_area'] = price_num/size_num
        yield item 
        pass
    
    
        
        