# -*- coding: utf-8 -*-
"""
Created on Mon Nov 26 11:52:34 2018

@author: jwjiang
"""

from selenium import webdriver
import time
import requests
import urllib
from bs4 import BeautifulSoup as bs
import re
import os

# ****************************************************
base_url_part1 = 'https://www.google.com/search?q='
base_url_part2 = '&source=lnms&tbm=isch'  # base_url_part1以及base_url_part2都是固定不变的，无需更改
#search_query = '工地 建筑工人'  # 检索的关键词，可自己输入你想检索的关键字
location_driver = '/usr/bin/chromedriver'  # Chrome驱动程序在电脑中的位置


class Crawler:
    #def __init__(self):


    # 启动Chrome浏览器驱动
    def start_brower(self):
        # 启动Chrome浏览器
        driver = webdriver.Chrome(location_driver)
        # 最大化窗口，因为每一次爬取只能看到视窗内的图片
        driver.maximize_window()
        # 浏览器打开爬取页面
        search_query = input('Please Input Keyword:')
        self.url = base_url_part1 + search_query + base_url_part2
        driver.get(self.url)
        return driver

    def downloadImg(self, driver):
        t = time.localtime(time.time())
        #foldername = str(t.__getattribute__("tm_year")) + "-" + str(t.__getattribute__("tm_mon")) + "-" + str(
            #t.__getattribute__("results1"))  # 定义文件夹的名字
        #picpath = '/home/kuangrx/pics/results1/%s' % (foldername)  # 下载到的本地目录
        picpath = r'/home/kuangrx/pics/results_google_en2/'
        if not os.path.exists(picpath):  # 路径不存在时创建一个
            os.makedirs(picpath)
        # 下载图片的本地路径 D:/ImageDownload/~~

        # 记录下载过的图片地址，避免重复下载
        img_url_dic = []
        x = 0
        # 当鼠标的位置小于最后的鼠标位置时,循环执行
        pos = 0
        for i in range(0, 2000):  # 此处可自己设置爬取范围
            pos = i * 500  # 每次下滚500
            if(driver.find_element_by_xpath('//a[@class="ksb"]')):
                driver.find_element_by_xpath('//a[@class="ksb"]').click()
            js = "document.documentElement.scrollTop=%d" % pos
            driver.execute_script(js)
            #time.sleep(2)
            # 获取页面源码
            html_page = driver.page_source
            # 利用Beautifulsoup4创建soup对象并进行页面解析
            soup = bs(html_page, "html.parser")
            # 通过soup对象中的findAll函数图像信息提取
            # imglist = soup.findAll('img', {'class': 'rg_ic rg_i'})
            print('soup Done.Num: %s' % i)
            # imglist = soup.findAll('div', {'class': 'rg_meta notranslate'})
            imglist = soup.findAll('div', {'class': 'rg_meta notranslate'})
            #print(imglist)
            print('divNum:',len(imglist))
            # ??这段代码问题?
            for imgurl in imglist:
                # print('imgurl',imgurl)
                imgurl_str = str(imgurl)
                # print('imgurl_str:', imgurl_str)
                start = imgurl_str.find(r'"ou":"')
                # print('start',start)
                end = imgurl_str.find(r'","ow":')
                # print('end',end)
                finalUrl = imgurl_str[start+6:end]
                # print('finnalUrl:',finalUrl)
                judge = 0
                try:
                    #print(x, end=' ')
                    #if imgurl['src'] not in img_url_dic:
                    if finalUrl not in img_url_dic:
                        target = picpath + '%s' % x
                        # print ('Downloading image to location: ' + target + '\nurl=' + imgurl['src'])
                        #img_url_dic[imgurl['src']] = r'/home/kuangrx/pics/results_google'
                        img_url_dic.append(finalUrl)
                        #urllib.request.urlretrieve(imgurl['src'], target)
                        #urllib.request.urlretrieve(finalUrl, target)
                        try:
                            res = requests.get(finalUrl, timeout=15)
                            if (str(res.status_code)[0] == "4" or str(res.status_code)[0] == "5" or str(res.status_code) == "204" or str(res.status_code) == "205"):
                                print(str(res.status_code), ":", finalUrl)
                                # return False
                                judge = 1
                            if (judge == 0):
                                with open(target, "wb") as f:
                                    f.write(res.content)
                                    print('已下载 %s 张, URL: %s' % (x + 1, finalUrl))
                                    x += 1
                        except Exception as e:
                            print("抛出异常：", finalUrl)
                            print(e)
                            # return False
                        #time.sleep(0.1)
                except KeyError:
                    print("KeyERROR!")
                    break

    def run(self):
        print()

        driver = self.start_brower()
        self.downloadImg(driver)
        driver.close()
        print("Download has finished.")


if __name__ == '__main__':
    craw = Crawler()
    craw.run()
