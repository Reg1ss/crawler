import os
import time
import urllib
from scrapy import Selector
from selenium import webdriver


class GoogleImgCrawl:
    def __init__(self):
        self.browser = webdriver.Chrome('/home/kuangrx/下载/chromedriver')
        self.browser.maximize_window()
        self.key_world = input('Please input the content of the picture you want to grab >:')
        self.img_path = r'/home/kuangrx/pics/results_google_en'  # 下载到的本地目录
        if not os.path.exists(self.img_path):  # 路径不存在时创建一个
            os.makedirs(self.img_path)

    def start_crawl(self):
        self.browser.get('https://www.google.com/search?q=%s' % self.key_world)
        self.browser.implicitly_wait(3)  # 隐形等待时间
        self.browser.find_element_by_xpath('//a[@class="iu-card-header"]').click()  # 找到图片的链接点击进去
        time.sleep(3)  # 休眠3秒使其加载完毕
        img_source = self.browser.page_source
        img_source = Selector(text=img_source)
        self.img_down(img_source)  # 第一次下载图片
        self.slide_down()  # 向下滑动继续加载图片

    def slide_down(self):
        for i in range(7, 20):  # 自己可以任意设置
            pos = i * 500  # 每次向下滑动500
            js = "document.documentElement.scrollTop=%s" % pos
            self.browser.execute_script(js)
            time.sleep(3)
            img_source = Selector(text=self.browser.page_source)
            self.img_down(img_source)

    def img_down(self, img_source):
        img_url_list = img_source.xpath('//div[@class="THL2l"]/../img/@src').extract()
        for each_url in img_url_list:
            if 'https' not in each_url: #仅仅就第一页可以，其他误判这个代码不是完整的是作者的错代码。
                # print(each_url)
                each_img_source = urllib.request.urlretrieve(each_url,
                                                             '%s/%s.jpg' % (self.img_path, time.time()))  # 储存图片


if __name__ == '__main__':
    google_img = GoogleImgCrawl()
    google_img.start_crawl()
