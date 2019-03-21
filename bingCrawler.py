import urllib
import requests
import os
import time
from bs4 import BeautifulSoup

def FindLink(PageNum, InputData):
    errorUrl = os.path.join("/home/kuangrx/pics/logs/", 'bings_en2_errorUrl.txt')
    # 记录下载过的图片地址，避免重复下载
    img_url_dic = []
    x = 0
    repeatNum = 0
    errorNum = 0
    for i in range(0,PageNum):
        try:
            if((i+1)%3==0):
                time.sleep(3)
            url = 'http://cn.bing.com/images/async?q={0}&first={1}&count=35&relp=35&lostate=r&mmasync=1&dgState=x*175_y*848_h*199_c*1_i*106_r*0'
            # 定义请求头
            agent = {
                'User-Agent': "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.165063 Safari/537.36 AppEngine-Google."}
            page1 = urllib.request.Request(url.format(InputData, i * 35 + 1))
            page = urllib.request.urlopen(page1)
            soup = BeautifulSoup(page.read(), 'html.parser')
            imglist = soup.findAll('a', {'class': 'iusc'})
            print('url: %s'%url.format(InputData, i * 35 + 1))
            print("soup Done.Num: %s. Total: %s. Error: %s. Repeat: %s" % (i, len(imglist),errorNum,repeatNum))
            # print('imglist_Num：', imglist)
            for imgurl in imglist:
                imgurl_str = str(imgurl['href'])
                print('imgurl_str',imgurl_str)
                if(imgurl_str.find(r'https%3a%2f%2f')):
                    start = imgurl_str.find(r'https%3a%2f%2f')
                if(imgurl_str.find(r'http%3a%2f%2f') and imgurl_str.find(r'https%3a%2f%2f')==-1):
                    start = imgurl_str.find(r'http%3a%2f%2f')
                if(imgurl_str.find(r'.jpg')):
                    end = imgurl_str.find(r'.jpg') + 4
                if(imgurl_str.find(r'.jpeg') and imgurl_str.find(r'.jpg')==-1):
                    end = imgurl_str.find(r'.jpeg') + 5
                if (imgurl_str.find(r'.png') and imgurl_str.find(r'.jpg')==-1 and imgurl_str.find(r'.jpeg')==-1):
                    end = imgurl_str.find(r'.png') + 4
                if (imgurl_str.find(r'.svg') and imgurl_str.find(r'.jpg')==-1 and imgurl_str.find(r'.jpeg')==-1 and imgurl_str.find(r'.png')==-1):
                    end = imgurl_str.find(r'.svg' ) + 4
                if (imgurl_str.find(r'.svg')==-1 and imgurl_str.find(r'.jpg')==-1 and imgurl_str.find(r'.jpeg')==-1 and imgurl_str.find(r'.png')==-1):
                    errorNum += 1
                    continue
                # print('end: ',end)
                url_1st = imgurl_str[start:end]
                print('url_1st: ',url_1st)
                finalUrl = url_1st.replace(r'%3a%2f%2f',r'://').replace('%2f','/')
                print("finalUrl ",finalUrl)
                judge = 0
                try:
                    if finalUrl not in img_url_dic:
                        target = r'/home/kuangrx/pics/results_bings_en2/' + '%s' % x
                        img_url_dic.append(finalUrl)
                        try:
                            res = requests.get(finalUrl, timeout=15)
                            if (str(res.status_code)[0] == "4" or str(res.status_code)[0] == "5" or str(res.status_code) == "204" or str(res.status_code) == "205"):
                                print(str(res.status_code), ":", finalUrl)
                                judge = 1
                                errorNum += 1
                                with open(errorUrl, "a", encoding="utf-8") as f:
                                    f.write(finalUrl + '\n')
                            if (judge == 0):
                                with open(target, "wb") as f:
                                    f\
                                        .write(res.content)
                                    print('已下载 %s 张, URL: %s' % (x + 1, finalUrl))
                                    x += 1
                        except Exception as e:
                            print("抛出异常：", finalUrl)
                            with open(errorUrl, "a", encoding="utf-8") as f:
                                f.write(finalUrl + '\n')
                            errorNum += 1
                            print(e)
                    else:
                        repeatNum += 1
                        print("Repeated!")
                except KeyError:
                    print("KeyERROR!")
                    break


            # 创建文件夹
            # if not os.path.exists("./" + word):
            #     os.mkdir('./' + word)

            # for StepOne in soup.select('.mimg'):
            #     link = StepOne.attrs['src']
            #     count = len(os.listdir('/home/kuangrx/pics/results_bings')) + 1
            #     SaveImage(link, word, count)
        except:
            print('URL OPENING ERROR !')
    with open(errorUrl, "a", encoding="utf-8") as f:
        f.write("soup Done.Num: %s. Total: %s. Error: %s. Repeat: %s" % (i, len(imglist),errorNum,repeatNum))

if __name__=='__main__':
    #输入需要加载的页数
    PageNum = 50
    #输入需要搜索的关键字
    word='construction site construction worker'
    #UTF-8编码
    InputData=urllib.parse.quote(word)
    print("ParseWord:",InputData)
    FindLink(PageNum,InputData)
