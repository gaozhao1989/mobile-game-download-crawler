from urllib.parse import urljoin
import scrapy
from ..items import GamedownloadItem


class GameDownloadSpider(scrapy.Spider):

    name = 'gameDownload'
    base_url = 'https://www.changgame.com'
    categoary_url = '{}/{categoary}'.format(base_url)
    ajax_page_url = '{}/game/ajaxGameList?{cid_chema}page={page_id}'.format(base_url)
    game_url = '{}/game/{game_id}.html'.format(base_url)
    categoary = {'items': [
        {'url': '', 'cid': ''},
        {'url': 'game.html', 'cid': ''},
        {'url': 'doudizhu.html', 'cid': '11'},
        {'url': 'majiang.html', 'cid': '12'},
        {'url': 'buyu.html', 'cid': '13'},
        {'url': 'zhajinhua.html', 'cid': '14'},
        {'url': 'niuniu.html', 'cid': '17'},
        {'url': 'shuiguo.html', 'cid': '19'},
        {'url': 'jieji.html', 'cid': '20'},
        {'url': 'xiuxian.html', 'cid': '1'},
        {'url': 'qipai.html', 'cid': '2'},
        {'url': 'shot.html', 'cid': '3'},
        {'url': 'online.html', 'cid': '4'},
        {'url': 'race.html', 'cid': '5'},
        {'url': 'maoxian.html', 'cid': '6'},
        {'url': 'jinying.html', 'cid': '7'}
    ]}

    # refrence https://github.com/Python3WebSpider/Weibo/blob/master/weibo/spiders/weibocn.py
    def start_requests(self):
        for item in self.categoary['items']:
            url = urljoin(self.address, item['url'])
            cid_params = 'cId={}&' if item['cid'] else ''
            ajax_schema = '/game/ajaxGameList?{}page='.format(cid_params)
            
        for url in urls:
            url = urljoin(self.address, url)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for game_url in response.xpath('//a[contains(@href,"game")]').re('/game/(\d+).html'):

            # item = GamedownloadItem()
            # item['game_id'] = response.xpath('//a[contains(@href,"game")]').re('/game/(\d+)')
            # yield item
