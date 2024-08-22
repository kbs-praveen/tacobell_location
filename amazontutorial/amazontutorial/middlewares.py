# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
import time
import random

from scrapy.http import HtmlResponse

class SeleniumMiddleware:
    def __init__(self):
        path = 'C:/Users/user/Downloads/chromedriver-win64/chromedriver-win64/chromedriver.exe'
        if not os.path.isfile(path):
            raise FileNotFoundError(f"ChromeDriver not found at path: {path}")

        service = Service(executable_path=path)
        chrome_options = Options()
        # Allow geolocation
        chrome_options.add_experimental_option("prefs", {
            "profile.default_content_setting_values.geolocation": 1  # 1 means allow
        })
        chrome_options.add_argument('--window-size=800,1280')


        # Additional options
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--log-level=3')
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        # Set a default geolocation (for example, San Francisco, CA, USA)
        self.set_denver_geolocation()

    def set_denver_geolocation(self):
        # Set geolocation for Denver, CO, USA
        self.driver.execute_cdp_cmd("Page.setGeolocationOverride", {
            "latitude": 38.3032,
            "longitude": -77.4605,
            "accuracy": 100
        })

    def process_request(self, request, spider):
        if request.meta.get('selenium'):
            self.driver.get(request.url)
            spider.logger.info(f"Opened {request.url}")
            self._scroll_to_load_content()
            self._wait_for_images()
            body = self.driver.page_source
            # Create the response object without the 'meta' argument
            response = HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)
            response.meta['driver'] = self.driver  # Attach driver to the response meta
            return response
        elif "tacobell.com/food" in request.url:
            self.driver.get(request.url)
            self._scroll_to_load_content()
            self._wait_for_images()
            body = self.driver.page_source
            return HtmlResponse(url=request.url, body=body, encoding='utf-8', request=request)

    def _scroll_to_load_content(self):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Adjust as needed
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

    def _wait_for_images(self):
        images = self.driver.find_elements(By.TAG_NAME, 'em')
        for em in images:
            if not em.get_attribute('complete'):
                self.driver.execute_script("arguments[0].scrollIntoView();", em)
                time.sleep(1)  # Adjust wait time if needed

    def spider_closed(self, spider):
        self.driver.quit()


class AmazontutorialSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class AmazontutorialDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
