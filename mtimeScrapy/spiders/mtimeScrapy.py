from scrapy import Spider, Request
from mtimeScrapy.items import MtimescrapyItem
from mtimeScrapy.spiders.wzApi import wzAPI

class mtimeScrapy(Spider):
    name = 'mtimeScrapy'
    start_urls = 'http://movie.mtime.com/'

    movie_id = '225925' # 这是“狂暴巨兽”这部电影的id，不同的电影id不同

    # 提取出代表页面的不同部分，使得构建下一页的url更方便
    # 这里出现了一个失误。。解析网页的时候发现其实下一页的按钮可以直接跳转到下一页页面，这个分割没什么作用
    middle_url_part = "/reviews/short/new"
    end_url_part = '.html'

    # 这是短评的第一页url，处理完之后进入下一页
    comment_url = start_urls + movie_id + middle_url_part + end_url_part

    def start_requests(self):
        yield Request(self.comment_url, callback=self.parse)


    def parse(self, response):
        # print(response.text)

        # 通过xpth定位全部短评
        for each_comment in response.xpath('//div[@class="mod_short"]'):
            item = MtimescrapyItem()

            # 电影的名称
            movie = response.xpath('//*[@id="db_sechead"]/div[2]/div/h1/a/text()').extract()[0]

            # 电影的评论
            comment = each_comment.xpath('.//h3/text()').extract()[0]

            # 电影的评分
            score = each_comment.xpath('.//span[@class="db_point ml6"]/text()').extract()[0]

            # 这条评论的时间，但这个应该是js动态加载的，但不知道为什么可以直接被解析出来
            time = each_comment.xpath('.//div[@class="mt10"]/a/@entertime').extract()[0]

            # print(movie + '/t' + comment + '/t' + score + '\n')

            item['movie'] = movie
            item['comment'] = comment
            item['score'] = score
            item['time'] = time

            positive, negative = wzAPI(comment)

            item['positive'] = positive
            item['negative'] = negative

            yield item



        # 判断还有没有下一页，没有下一页时网页的属性值是mr10 false，有的话是ml10 next，不过这里好像出了点问题。。。代码段没有执行，后续要填坑
        next = response.xpath('//div[@id="PageNavigator"]/a')
        for each_next in next:
            if each_next.xpath('.//@class').extract()[0] == 'mr10 next':
                next_url = each_next.xpath('.//@href').extract()[0]
                print(next_url)
                yield Request(next_url, callback=self.parse)
            else:
                pass



