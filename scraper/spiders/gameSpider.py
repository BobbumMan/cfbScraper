import scrapy
import re
from scraper.items import GameItem

year = 2015

class cfbSpider(scrapy.Spider):
    name = "cfb"
    allowed_domains = ["espn.go.com"]
    start_urls = [
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/1",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/2",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/3",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/4",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/5",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/6",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/7",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/8",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/9",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/10",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/11",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/12",
        "http://espn.go.com/college-football/scoreboard/_/group/80/year/"+str(year)+"/seasontype/2/week/13",
    ]

    def parse(self, response):
        name_re = '\"location\"\:\"(\D+?(?:\\u00e9)?\D+?)\"'
	box_re = '\"href\"\:\"(http\:\/\/espn\.go\.com\/college\-football\/boxscore\?.*?)\"'
	date_re = '\"date\"\:\"(\d+\-\d+\-\d+)'
	regex_str = name_re + '.*?' + name_re + '.*?' + box_re + '.*?' + date_re
	script_blocks = response.xpath('//script[not(@*)]')
	# game info storage
	boxscore_links = []
	home = []
	away = []
	dates = []
	# find games and links
	for block in script_blocks:
		block_links = block.re(regex_str)
		counter = 0
		for link in block_links:
			if counter == 0:
				home.append(re.sub('\\\u00e9','e',link))
			elif counter == 1:
				away.append(re.sub('\\\u00e9','e',link))
			elif counter == 2:
				boxscore_links.append(link)
			elif counter == 3:
				dates.append(re.sub('-','',link))
			# count to track what data type (uuugly)
			counter += 1
			if counter == 4:
				counter = 0
	for index, boxscore_link in enumerate(boxscore_links):
		game = GameItem()
		game['home'] = home[index]
		game['away'] = away[index]
		game['date'] = dates[index][:4] + '-' + dates[index][4:6] + '-' + dates[index][6:]
		game['_id'] = re.search('(\d+)', boxscore_link).group(0)
		yield game
		
