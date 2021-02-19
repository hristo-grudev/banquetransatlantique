import scrapy

from scrapy.loader import ItemLoader
from ..items import BanquetransatlantiqueItem
from itemloaders.processors import TakeFirst


class BanquetransatlantiqueSpider(scrapy.Spider):
	name = 'banquetransatlantique'
	start_urls = ['https://www.banquetransatlantique.lu/fr/index.html']

	def parse(self, response):
		post_links = response.xpath('//article//a[@class="more"]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@itemprop="articleBody"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()

		item = ItemLoader(item=BanquetransatlantiqueItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)

		return item.load_item()
