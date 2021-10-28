import re
import os
import scrapy
from ..items import AbcdItem
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from scrapy.utils.project import get_project_settings



class Test1Spider(scrapy.Spider):
    name = 'test1'
    #allowed_domains = ['youtube.com']
    #start_urls = ['https://www.youtube.com/watch?v=cm4lkqt647U']

    def start_requests(self):
        settings= get_project_settings()
        driver_path = 'C:\chromedriver\chromedriver.exe'
        options= webdriver.ChromeOptions()
        options.headless = True
        driver = webdriver.Chrome(driver_path, options=options)
        driver.get('https://www.youtube.com/')
        link_elements = driver.find_elements_by_xpath('//*[@id="thumbnail"][text()]')
        for link in link_elements:
            # yield scrapy.Request(link.get_attribute('href'), callback=self.parse)
            link = link.get_attribute('href')
            yield SeleniumRequest(
                url = link,
                wait_time = 2,
                screenshot = True,
                callback = self.parse,
                dont_filter = True)
        driver.quit()

    def parse(self, response):
        name = response.xpath('//h1[@class="title style-scope ytd-video-primary-info-renderer"]/yt-formatted-string/text()').get()
        item = AbcdItem()
        item['name'] = name
        yield item




