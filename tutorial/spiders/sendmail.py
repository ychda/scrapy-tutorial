# -*- coding: utf-8 -*-
# toto 无法正常发送邮件，什么情况？
import scrapy
from tutorial import settings


class SendmailSpider(scrapy.Spider):
    name = 'sendmail'
    allowed_domains = ['books.toscrape.com']
    start_urls = ['http://books.toscrape.com/']

    def parse(self, response):
        for href in response.xpath('//section/div/ol[@class="row"]/li').css('.image_container a::attr(href)'):
            yield response.follow(href, self.parse_book)

        next_page = response.css('.pager .next a::attr(href)').get()
        # if next_page is not None:
        if next_page is None:
            yield response.follow(next_page, self.parse)

    def parse_book(self, response):
        yield {
            'title': response.css('article.product_page .product_main h1::text').get(),
            'price': response.css('article.product_page .product_main p.price_color::text').get(),
            'url': response.url,
            'UPC': response.xpath('//table[@class="table table-striped"]/tr/td/text()').get(),  # tbody呢？
        }

    # https://scrapy.readthedocs.io/en/latest/topics/email.html#mailsender-class-reference
    def close(self, reason):
        from scrapy.mail import MailSender
        # mailer = MailSender.from_settings(settings)
        """
        mailer = MailSender(
            smtphost=settings.MAIL_HOST,
            mailfrom=settings.MAIL_FROM,
            smtpuser=settings.MAIL_HOST,
            smtppass=settings.MAIL_PASS,
            smtpport=settings.MAIL_PORT,
            smtptls=settings.MAIL_TLS,
            smtpssl=settings.MAIL_SSL,
        )
        """
        mailer = MailSender(
            smtphost='smtp.qq.com',
            mailfrom='ychda@qq.com',
            smtpuser='ychda@qq.com',
            smtppass='password',
            smtpport=465,
            smtptls=False,
            smtpssl=True,
        )
        mailer.send(to=["ychda@qq.com"],
                    subject="subject",
                    body="body",
                    cc=["ychda@ychda.cn"],
                    charset='utf-8')
