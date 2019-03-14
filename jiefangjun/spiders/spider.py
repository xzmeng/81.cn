# -*- coding: utf-8 -*-
import scrapy


class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['81.cn']
    start_urls = []

    def start_requests(self):
        url_fmt = 'http://www.81.cn/jfjbmap/content/{}-{}/{}/node_2.htm'
        for year in range(2014, 2020):
            year = str(year)
            for month in range(3, 13):
                month = '0' + str(month) if month < 10 else month
                for day in range(1, 32):
                    day = '0' + str(day) if day < 10 else day
                    meta = {
                        'year': year,
                        'month': month,
                        'day': day
                    }
                    if year == '2014' and int(month) < 7:
                        continue
                    url = url_fmt.format(str(year), str(month), str(day))
                    yield scrapy.Request(url, self.parse, meta=meta)

    def parse(self, response):
        meta = response.meta
        if meta['year'] in ('2014', '2015'):
            channel_list = response.css('#pageLink')
        else:
            channel_list = response.css('.channel-list li a')
        for i, channel in enumerate(channel_list, start=1):
            category = channel.css('::text').get()
            url = channel.css('::attr(href)').get()
            meta['category'] = category
            meta['category_no'] = i
            yield response.follow(url, meta=meta, callback=self.parse_channel, dont_filter=True)


    def parse_channel(self, response):
        meta = response.meta
        if meta['year'] in ('2014', '2015'):
            items = response.css('.con001 a')
            for i, item in enumerate(items, start=1):
                url = item.css('::attr(href)').get()
                title = item.css('div::text').get()
                meta['title'] = title
                meta['article_no'] = i
                yield response.follow(url, meta=meta, callback=self.parse_text)
        else:
            items = response.css('.newslist-item.current li a')
            for i, item in enumerate(items, start=1):
                url = item.css('::attr(href)').get()
                title = item.css('::text').get()
                meta = response.meta

                meta['title'] = title
                meta['article_no'] = i
                yield response.follow(url, meta=meta, callback=self.parse_text)

    def parse_text(self, response):
        meta = response.meta
        article = response.css('founder-content p::text').getall()
        meta['subtitle'] = response.css('.subtitle::text').get()
        meta['introtitle'] = response.css('.introtitle::text').get()
        meta['author'] = response.css('.author::text').get()
        ps = []
        for p in article:
            p = p.strip()
            if p:
                ps.append(p)
        meta['ps'] = ps
        yield meta






