import re
import scrapy
from ..items import GamedownloadItem


class GameDownloadSpider(scrapy.Spider):

    name = 'gameDownload'
    start_url = 'https://www.changgame.com/'
    game_list_url = 'https://www.changgame.com{game_list_url}'
    game_url = 'https://www.changgame.com{game_url}'
    game_download_url = 'https://www.changgame.com/game/{platform}/down/{game_id}.html'
    game_logo_url = 'https://www.changgame.com{game_logo_url}'

    def start_requests(self):
        yield scrapy.Request(self.start_url, callback=self.parse)

    def parse(self, response):
        # game category
        for game_lis in response.xpath('//div[contains(@class, "nav")]/ul/li[@class="swiper-slide"]'):
            rel_game_list_url = game_lis.xpath('./a/@href').extract_first()
            abs_game_list_url = self.game_list_url.format(
                game_list_url=rel_game_list_url)
            yield scrapy.Request(abs_game_list_url, callback=self.parse_game_list)
        # hot recommand
        for game in response.xpath('//div[contains(@class, "lefttjbox") and contains(@class, "swiper-slide")]/ul/li'):
            rel_game_url = game.xpath('./a/@href').extract_first()
            abs_game_url = self.game_url.format(game_url=rel_game_url)
            yield scrapy.Request(abs_game_url, callback=self.parse_game)
        # everyone play
        for game in response.xpath('//div[contains(@class, "rightcontent")]/div[@class="rightall"]/div[@class="rightlist"]'):
            rel_game_url = game.xpath(
                './div[@class="rightalldown"]/a/@href').extract_first()
            abs_game_url = self.game_url.format(game_url=rel_game_url)
            yield scrapy.Request(abs_game_url, callback=self.parse_game)
        # today's recommand
        rel_today_recommand_game_url = response.xpath(
            '//div[@class="newrightbox"]/a').extract_first()
        abs_today_recommand_game_url = self.game_url.format(
            game_url=rel_today_recommand_game_url)
        yield scrapy.Request(abs_today_recommand_game_url, callback=self.parse_game)
        # bottom games
        for game in response.xpath('//div[@class="hrefbox"]/ul/li'):
            rel_game_url = game.xpath('./a/@href').extract_first()
            abs_game_url = self.game_url.format(game_url=rel_game_url)
            yield scrapy.Request(abs_game_url, callback=self.parse_game)

    def parse_game_list(self, response):
        # game in category list
        for game in response.xpath('//div[contains(@class, "pagelistbox") and contains(@class, "swiper-slide")]//div[@class="boutiquelogo"]'):
            rel_game_url = game.xpath('./a/@href').extract_first()
            abs_game_url = self.game_url.format(game_url=rel_game_url)
            yield scrapy.Request(abs_game_url, callback=self.parse_game)
        # game in bottom
        for game in response.xpath('//div[@class="hrefbox"]/ul/li'):
            rel_game_url = game.xpath('./a/@href').extract_first()
            abs_game_url = self.game_url.format(game_url=rel_game_url)
            yield scrapy.Request(abs_game_url, callback=self.parse_game)

    def parse_game(self, response):
        item = GamedownloadItem()
        item['gameId'] = re.search(
            'https://www.changgame.com/game/(\d+).html', response.request.url).group(1)
        item['name'] = response.xpath(
            '//div[@class="introduce-name"]/h2/text()').extract_first()
        item['logoUrl'] = self.game_logo_url.format(game_logo_url=response.xpath(
            '//div[@class="introduce"]/img/@src').extract_first())
        item['desc'] = response.xpath(
            '//div[@class="game-left-intro"]/text()').extract_first()
        item['screenCapture'] = response.xpath(
            '//div[@class="game-left-news"]//li[contains(@class, "swiper-slide")]/img/@src').extract()
        item['score'] = response.xpath(
            '//span[@class="score"]/text()').extract_first()
        item['category'] = response.xpath(
            '//div[@class="load-code-right"]/p[3]/a/text()').extract_first()
        item['keyWord'] = response.xpath('//div[@class="load-code-right"]/p[4]/span/text()').extract()
        try:
            size = re.search('(\d+).(\d+)MB', response.xpath(
                '//div[@class="load-code-right"]/p[5]/text()').extract_first()).group()
        except AttributeError:
            size = None
        item['size'] = size
        try:
            re.search(item['gameId'], response.xpath(
                '//div[@class="code-list android-wrap"]/img/@src').extract_first()).group()
            downloadUrl = self.game_download_url.format(
                platform='android', game_id=item['gameId'])
        except AttributeError:
            downloadUrl = None
        item['androidDownloadUrl'] = downloadUrl
        try:
            re.search(item['gameId'], response.xpath(
                '//div[@class="code-list ios-wrap"]/img/@src').extract_first()).group()
            downloadUrl = self.game_download_url.format(
                platform='ios', game_id=item['gameId'])
        except AttributeError:
            downloadUrl = None
        item['iosDownloadUrl'] = downloadUrl
        yield item
