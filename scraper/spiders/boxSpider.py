import scrapy
import pymongo
from scraper.items import BoxItem

pymongo.MongoClient('mongodb://localhost:27017')['cfb']['box_scores'].drop()

def parseRushing(item, div):
  item['carries'] = div.xpath('.//td[@class="car"]/text()').extract()[0]
  item['rushing_yards'] = div.xpath('.//td[@class="yds"]/text()').extract()[0]
  item['rushing_tds'] = div.xpath('.//td[@class="td"]/text()').extract()[0]

base_url = "http://espn.go.com/college-football/boxscore?gameId="

class boxSpider(scrapy.Spider):
  name = "box"
  allowed_domains = ['espn.go.com']
  start_urls = []
  cursor = pymongo.MongoClient('mongodb://localhost:27017')['cfb']['games'].find()
  for record in cursor:
    start_urls.append(base_url + str(record['_id']))
    
  def parse(self, response):
    
    item_home = BoxItem()
    item_away = BoxItem()
    
    item_home['team_name'] = response.xpath('//div[@id="gamepackage-header-wrap"]//div[@class="team home"]//span[@class="long-name"]/text()').extract()[0]
    item_away['team_name'] = response.xpath('//div[@id="gamepackage-header-wrap"]//div[@class="team away"]//span[@class="long-name"]/text()').extract()[0]
    
    item_home['position'] = "home"
    item_away['position'] = "away"
    
    rushinghome = response.xpath('//div[@id="gamepackage-rushing"]//div[contains(@class,"gamepackage-home-wrap")]//tr[@class="highlight"]')
    rushingaway = response.xpath('//div[@id="gamepackage-rushing"]//div[contains(@class,"gamepackage-away-wrap")]//tr[@class="highlight"]')
    parseRushing(item_home, rushinghome)
    parseRushing(item_away, rushingaway)
    yield item_home
    yield item_away
