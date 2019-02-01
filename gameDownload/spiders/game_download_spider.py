from urllib.parse import urljoin
import scrapy
from ..items import GamedownloadItem

class GameDownloadSpider(scrapy.Spider):

    name = 'gameDownload'
    address = 'https://www.changgame.com/'

    def start_requests(self):
        urls = [
            '',
            'game.html',
            'doudizhu.html',
            'majiang.html',
            'buyu.html',
            'zhajinhua.html',
            'niuniu.html',
            'shuiguo.html',
            'jieji.html',
            'xiuxian.html',
            'qipai.html',
            'shot.html',
            'online.html',
            'race.html',
            'maoxian.html',
            'jinying.html'
        ]
        for url in urls:
            url = urljoin(self.address, url)
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        item = GamedownloadItem()
        item['game_id'] = response.xpath('//a[contains(@href,"game")]').re('/game/(\d+)')
        yield item