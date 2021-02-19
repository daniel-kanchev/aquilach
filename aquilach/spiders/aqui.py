import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from aquilach.items import Article


class AquiSpider(scrapy.Spider):
    name = 'aqui'
    start_urls = ['https://www.aquila.ch/blog/']

    def parse(self, response):
        links = response.xpath('//h3/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

        next_page = response.xpath('//li[@class="page-next"]/a/@href').get()
        if next_page:
            yield response.follow(next_page, self.parse)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1//text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//div[@class="date-info"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="uncode_text_column"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
