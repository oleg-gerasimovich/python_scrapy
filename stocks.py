import scrapy
from scrapy.selector import Selector


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    start_urls = ['https://www.centraldepo.by/helpserv/emitent/']

    def parse(self, response):
        data = response.css('div.em_dep_info')
        
        for item in data:
            necessary_data = {}
            for table in item.css('table'):
                for row in table.css('tr'):
                    body = row.extract()
                    key = Selector(text=body).xpath('//td[1]/text()').get()
                    value = Selector(text=body).xpath('//td[2]/text()').get()
                    necessary_data[key] = value
            

            item_stocks_and_bonds = [x for x in item.css('h4::text').getall()]
            check_for_stocks_and_bonds = ['Акции', 'Облигации']

            for position in check_for_stocks_and_bonds:
                if position in item_stocks_and_bonds:
                    necessary_data[position] = '+'
                else:
                    necessary_data[position] = '-'

            yield necessary_data
        
        pages = response.css('ul.pager li')
        next_page = pages[-1].css('a').attrib['href']
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
