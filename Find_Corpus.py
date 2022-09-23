


from ast import Raise
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import numpy as np
import os
import time
# Discuss 1:
# 只保留中文或英文的方法：
# https://blog.csdn.net/BurningSilence/article/details/118488543
# 
# 正则表达式
# https://blog.csdn.net/qq_44165157/article/details/122352738


# Discuss 2:
# 访问某个网站过多（或过快）时，会导致IP被封，
# 如 http://data.people.com.cn/rmrb/pd.html?qs=%7B%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&pageNo=1&pageSize=20&position=0

# Discuss 3：
# 如何保证下载快速且正确：
# 如D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\AvoidSame_all.txt
# 经验证，chrono下载也会存在丢包的现象

# Discuss 4：
# 页面等待了太长时间
# https://blog.csdn.net/weixin_41624982/article/details/89048936
# 核心是：
# browser.set_page_load_timeout(1)
# try:
#     browser.get(N1)
# except:
#     browser.execute_script("window.stop()")



# 显式等待
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# locator = (By.XPATH,'//*[@id="titleList"]/ul')
# WebDriverWait(browser,3,0.5).until(EC.presence_of_element_located(locator))
# papers = browser.find_elements(By.XPATH,'//*[@id="titleList"]/ul/li')




# https://www.bbiquge.net/book/24881/10446152.html
# https://www.bbiquge.net/book/24881/18556161.html
class Find_ChineseCorpus():
    def __init__(self) -> None:
        # 人民日报 -> 点击 人民日报图文数据库1946-2022 -> 右下角高级检索，得到目前使用的url
        # http://paper.people.com.cn/rmrb/html/2022-05/05/nbs.D110000renmrb_01.htm

        # http://data.people.com.cn/rmrb/s?type=2&qs=%7B%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D
        # http://data.people.com.cn/rmrb/s?qs=%7B%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&ss=1&pageNo=2&pageSize=20
        # http://data.people.com.cn/rmrb/s?qs=%7B%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&ss=1&pageNo=3&pageSize=20
        
        # 实际每篇文章的url：
        # http://data.people.com.cn/rmrb/pd.html?qs=%7B%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&pageNo=386&pageSize=20&position=0
        self.DownloadUrls = []
        self.words = []

        self.web = 'https://www.bbiquge.net/quanben/'
        self.BookUrls = []
        self.BookUrls_Path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\Biquge\BookUrls.txt'
        self.PagesUrls_path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\Biquge\Pages'
        self.Words_Path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\Biquge\Words'


        options = webdriver.ChromeOptions()
        User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36 Edg/96.0.1054.57'
        options.add_argument('user-agent=' + User_Agent)     # UA代理
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-gpu')
        # prefs = {'permissions.default.stylesheet':2,'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        prefs = {'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(options=options,service = Service(r'D:\chromedriver\chromedriver.exe'))

    def Create_DownloadUrl(self):
        for i in range(1,100000):
            kk = [f'http://data.people.com.cn/rmrb/pd.html?qs=%7B%22obs%22%3A%5B%7B%22fld%22%3A%22dataTime%22%2C%22drt%22%3A%22DESC%22%7D%5D%7D&tr=A&pageNo={i}&pageSize=20&position={j}' for j in range(20)]
            self.DownloadUrls.extend(kk)
        np.savetxt(r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\DownloadUrls.txt',self.DownloadUrls,fmt='%s')

    def Downwords(self):
        options = webdriver.ChromeOptions()
        User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36 Edg/96.0.1054.57'
        options.add_argument('user-agent=' + User_Agent)     # UA代理
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-gpu')
        # prefs = {'permissions.default.stylesheet':2,'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        prefs = {'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(options=options,service = Service(r'D:\chromedriver\chromedriver.exe'))

        n = 600
        for url in self.DownloadUrls[n:]:
            try:
                browser.get(url)
                time.sleep(0.1)
                links = browser.find_elements(By.XPATH,'//*[@id="FontZoom"]/p')
                # //*[@id="FontZoom"]/p[5]/b
                for link in links:
                    try:
                        word = link.find_element(By.XPATH,'.//b').text
                    except:
                        word = link.text
                    self.words.append(word)
            except:
                pass
            
            print(n)
            if n%10 == 0:
                np.savetxt(r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\Chinese_words_600.txt',self.words,fmt='%s')

            n += 1

    def GetBookUrls(self):
        browser = self.browser
        browser.get(self.web)
        links = browser.find_elements(By.XPATH,'//*[@id="main"]/div[3]/div/ul/li')
        # //*[@id="main"]/div[3]/div/ul/li[1]/span[1]/a
        for link in links:
            url_of_book = link.find_element(By.XPATH,'.//span[1]/a').get_attribute('href')
            self.BookUrls.append(url_of_book)
        np.savetxt(self.BookUrls_Path,self.BookUrls,fmt='%s')

    def GetPageUrls(self):
        browser = self.browser
        Books = np.loadtxt(self.BookUrls_Path,dtype=str)
        # print(len(Books)) # 41
        book_num = 25
        for book in Books[book_num:]:
            # Book url is:   https://www.bbiquge.net/book/24881/
            # Every page is: https://www.bbiquge.net/book/24881/index_2.html
            Pages_url = []
            for n in range(1,10000):
                browser.get(f'{book}/index_{n}.html')
                # enter every big page
                buton = browser.find_element(By.XPATH,'/html/body/div[4]/div/span[2]/a').get_attribute('href')
                # javascript:
                if buton != 'javascript:':
                    pages = browser.find_elements(By.XPATH,'/html/body/div[4]/dl/dd')
                    for page in pages:
                        link = page.find_element(By.XPATH,'.//a').get_attribute('href')
                        # link: every single page
                        Pages_url.append(link)
                else:
                    break
            print(book_num)
            np.savetxt(f'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\Biquge\Pages\{book_num}_Pages.txt',Pages_url,fmt='%s')
            book_num += 1

    def DownloadBiquge(self):
        import pathlib
        num = 1
        browser = self.browser
        for book in os.listdir(self.PagesUrls_path)[num-1:]:
            full_path = os.path.join(self.PagesUrls_path,book)
            urls = np.loadtxt(full_path,dtype=str)
            pathlib.Path(f'D:/Vscode_Programming_Set/WebCrawler/English&Chinese_Corpus/Chinese/Biquge/Words/{num}.txt').touch()
            for url in urls:
                try:
                    browser.get(url)
                    with open(f'D:/Vscode_Programming_Set/WebCrawler/English&Chinese_Corpus/Chinese/Biquge/Words/{num}.txt','a',encoding='utf-8') as f:
                        f.write(browser.find_element(By.XPATH,'//*[@id="content"]').text[50:])
                except:
                    pass
            print(num)
            num += 1

    def pure(self):
        import re
        for txt in os.listdir(self.Words_Path):
            full_path = os.path.join(self.Words_Path,txt)

            # PermissionError: [Errno 13] Permission denied: 'D:\\Vscode_Programming_Set\\WebCrawler\\English&Chinese_Corpus\\Chinese\\Biquge\\Words'
            with open(full_path,'r',encoding='utf-8') as f:
                data = f.read().splitlines()
            Init = ''.join(data)
            real = re.sub(u"([^\u4e00-\u9fa5])", "", Init)
            with open(r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\Biquge\Pure_Chinese_Words.txt','a',encoding='utf-8') as f:
                f.write(real)


class GuangMingRiBao():
    def __init__(self) -> None:
        
        # https://epaper.gmw.cn/gmrb/html/2020-09/08/nbs.D110000gmrb_01.htm
        self.FirstUrls = []
        self.FirstUrls_Path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\GuangMingRiBao\FirstUrls+.txt'
        self.LastUrls_Path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\GuangMingRiBao\LastUrls+.txt'
        self.Words_Path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\GuangMingRiBao\Words+.txt'

    def Create_FirstUrls(self):
        years = range(2011,2022)
        months = ['01','02','03','04','05','06','07','08','09','10','11','12']
        days = range(1,29)
        days = [str(i) for i in days]
        for i in range(9):
            days[i] = '0'+days[i]

        for year in years:
            for month in months:
                for day in days:
                    self.FirstUrls.append(f'https://epaper.gmw.cn/gmrb/html/{year}-{month}/{day}/nbs.D110000gmrb_01.htm')
        np.savetxt(self.FirstUrls_Path,self.FirstUrls,fmt='%s')

    def Get_LastUrls(self):
        import time
        FirstUrls = np.loadtxt(self.FirstUrls_Path,dtype=str)
        options = webdriver.ChromeOptions()
        User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36 Edg/96.0.1054.57'
        options.add_argument('user-agent=' + User_Agent)     # UA代理
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-gpu')
        prefs = {'permissions.default.stylesheet':2,'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        # prefs = {'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(options=options,service = Service(r'D:\chromedriver\chromedriver.exe'))
        browser.set_page_load_timeout(1)
        Last_urls = []
        start = time.time()
        for N1 in FirstUrls: # https://epaper.gmw.cn/gmrb/html/2020-06/28/nbs.D110000gmrb_01.htm
            try:
                browser.get(N1)
            except:
                browser.execute_script("window.stop()")
            # locator = (By.XPATH,'//*[@id="titleList"]/ul')
            # WebDriverWait(browser,3,0.5).until(EC.presence_of_element_located(locator))
            papers = browser.find_elements(By.XPATH,'//*[@id="titleList"]/ul/li')
            for paper in papers:
                Last_url = paper.find_element(By.XPATH,'.//a').get_attribute('href')
                Last_urls.append(Last_url)
            np.savetxt(self.LastUrls_Path,Last_urls,fmt='%s')
        end = time.time()
        aa = end-start
        print(f'The time is {aa}')

    def Download(self):
        # Define browser
        options = webdriver.ChromeOptions()
        User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36 Edg/96.0.1054.57'
        options.add_argument('user-agent=' + User_Agent)     # UA代理
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-gpu')
        prefs = {'permissions.default.stylesheet':2,'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        # prefs = {'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        options.add_experimental_option("prefs", prefs)
        browser = webdriver.Chrome(options=options,service = Service(r'D:\chromedriver\chromedriver.exe'))

        browser.set_page_load_timeout(1.5)
        LastUrls = np.loadtxt(self.LastUrls_Path,dtype=str)
        
        num = 1
        for url in LastUrls:
            Words = ''
            try:
                browser.get(url)
            except:
                browser.execute_script("window.stop()")
            try:
                locator = (By.XPATH,'//*[@id="articleContent"]')
                WebDriverWait(browser,3,0.5).until(EC.presence_of_element_located(locator))
                data = browser.find_elements(By.XPATH,'//*[@id="articleContent"]/p')
                for i in data:
                    try:
                        word = i.find_element(By.XPATH,'.//strong').text
                    except:
                        word = i.text
                    Words += word
                with open(self.Words_Path,'a',encoding='utf-8') as f:
                    f.write(Words)
                print(num)
                num += 1
            except:
                continue
    
    def pure(self):
        import re
        with open(self.Words_Path,'r',encoding='utf-8') as f:
            data = f.read().splitlines()
        Init = ''.join(data)
        real = re.sub(u"([^\u4e00-\u9fa5])", "", Init)
        with open(r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\GuangMingRiBao\Pure_Words_GuangMingRiBao.txt','w') as f:
            f.write(real)


class Find_EnglishCorpus():
    def __init__(self) -> None:
        self.web_list = ['http://novel.tingroom.com/jingdian/',\
                        'http://novel.tingroom.com/shuangyu/',\
                        'http://novel.tingroom.com/mingren/',\
                        'http://novel.tingroom.com/lizhi/',\
                        'http://novel.tingroom.com/duanpian/',\
                        'http://novel.tingroom.com/kehuan/',\
                        'http://novel.tingroom.com/ertong/',\
                        'http://novel.tingroom.com/zongjiao/']
        self.preurl_list = ['http://novel.tingroom.com/jingdian/list_1_',\
                            'http://novel.tingroom.com/shuangyu/list_33_',\
                            'http://novel.tingroom.com/mingren/list_32_',\
                            'http://novel.tingroom.com/lizhi/list_6_',\
                            'http://novel.tingroom.com/duanpian/list_31_',\
                            'http://novel.tingroom.com/kehuan/list_30_',\
                            'http://novel.tingroom.com/ertong/list_29_',\
                            'http://novel.tingroom.com/zongjiao/list_28_']
        self.cate_list = ['jingdian','shuangyu','mingren','lizhi','duanpian','kehuan','ertong','zongjiao']
        self.pages = [162,19,66,45,264,14,53,8]
        self.BookNum_dir = 'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Book_Num_url'
        self.BookDownload_url_dir = 'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Book_Download_url'
        self.BookSaved_dir = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\English_Corpus_Dir\Remain'
    # 在网站上找到每本书的url 如:http://novel.tingroom.com/kehuan/4753
    def Get_BookNum(self,cate:str,prurl,page):
        options = webdriver.ChromeOptions()
        User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.127 Safari/537.36 Edg/96.0.1054.57'
        options.add_argument('user-agent=' + User_Agent)     # UA代理
        options.add_argument("--window-size=1920,1080")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_argument('--disable-gpu')
        # prefs = {'permissions.default.stylesheet':2,'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        prefs = {'profile.managed_default_content_settings.images': 2}    # 禁用CSS样式表和图像
        options.add_experimental_option("prefs", prefs)
        self.browser = webdriver.Chrome(options=options,service = Service(r'D:\chromedriver\chromedriver.exe'))
        
        book_list = []
        for i in range(1,page+1):
            url = prurl+ f'{i}.html'
            self.browser.get(url)
            link_list = self.browser.find_elements(By.CLASS_NAME,'yuyu')
            for j in link_list:
                link = j.find_element(By.XPATH,".//a").get_attribute('href')
                book_list.append(link)
        np.savetxt(os.path.join(self.BookNum_dir,f'{cate}.txt'),book_list,fmt='%s')
    # 获取book的实际下载地址
    def Get_Downloadpath(self,BookNum_dir):
        # txt地址：    http://novel.tingroom.com/jingdian/5146
        # 实际下载地址：http://novel.tingroom.com/novel_down.php?aid=5146&dopost=txt
        for txt in os.listdir(BookNum_dir):
            down_list = np.loadtxt(os.path.join(BookNum_dir,txt),dtype=str)
            down_path = [f'http://novel.tingroom.com/novel_down.php?aid={i[i.rfind("/")+1:]}&dopost=txt' for i in down_list]
            np.savetxt(os.path.join(self.BookDownload_url_dir,f'{txt}.txt'),down_path,fmt='%s')
    def AvoidSame(self):
        all_data = []
        for i in os.listdir(self.BookDownload_url_dir):
            full_path = os.path.join(self.BookDownload_url_dir,i)
            data = np.loadtxt(full_path,dtype=str)
            all_data.extend(data)
        result = list(set(all_data))
        np.savetxt(os.path.join(self.BookDownload_url_dir,'AvoidSame_all.txt'),result,fmt = '%s')
    def Pure(self,dir_path):
        import re
        num = 1
        for txt in os.listdir(dir_path):
            with open(os.path.join(dir_path,txt),'r',encoding='utf-8') as f:
                data = f.read().splitlines()
            Init = ''.join(data)
            real = re.sub(u"([^\u0041-\u005a\u0061-\u007a])", "", Init)
            with open(r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\English_Corpus_Dir\Pure_English_Words\Pure_English_Words.txt','a',encoding='utf-8') as f:
                f.write(real)
            print(num)
            num += 1

    " The first version of downloading: "
    def Download_txt(self,down_txt,save_path):
        import requests
        down_list = np.loadtxt(down_txt,dtype=str)
        num = 1
        for i in down_list:
            while flag == 0:
                req = requests.get(i)
                if req.status_code != 200:
                    pass
                else:
                    with open(os.path.join(save_path,f'{num}.txt'),'wb') as f:
                        f.write(req.content)
                    flag = 1
                    print(num)
                    num += 1

class HJW_Process():
    def __init__(self) -> None:
        self.English_path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\English\English_Corpus_Dir\Pure_English_Words\Pure_English_Words.txt'
        self.Biquge_path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Chinese\Biquge\Pure_Words_Biquge.txt'
        self.GuangMingRiBao_path = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\GuangMingRiBao\Pure_Words_GuangMingRiBao.txt'

    def English(self):
        import string,math
        alphabet = list(string.ascii_lowercase)
        with open(self.English_path,'r') as f:
            all_data = f.read()
        
        all_data = all_data.lower()
        # All_data memory: 1374758 KB
        # All_data length: 1407751827
        length = len(all_data) 
        # 2048 / 1374758 * 1407751827
        sec = 2097151
        num = 1
        for _ in range(sec,length,sec):
            data = all_data[0:_]
            Fre = []
            for letter in alphabet:
                Fre.append(data.count(letter)/len(data))
            entropy = -sum([i*math.log2(i) for i in Fre])
            Fre.append(entropy)
            Fre = [str(i)[0:7] for i in Fre]
            Fre = ','.join(Fre) +'\n'
            with open(r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Final_Results\English.txt','a') as f:
                f.write(Fre)
            print(num)
            num += 1

    def Chinese(self,corpus:str):
        import math
        if corpus == 'GuangMingRiBao':
            path = self.GuangMingRiBao_path
            memory = 52216 # GuangMingRiBao: 52216 KB
        elif corpus == 'Biquge':
            path = self.Biquge_path
            memory = 102081 # Biquge: 102081 KB
        else:
            raise Exception('No such corpus')
        try:
            with open(path,'r',encoding='gbk') as f:
                all_data = f.read()
        except:
            with open(path,'r',encoding='utf-8') as f:
                all_data = f.read()
        sec = int(2048 / memory * len(all_data))
        for _ in range(sec,len(all_data),sec):
            data = all_data[0:_]
            database = set(data)
            length = len(data)
            Fre = [data.count(i)/length for i in database]
            entropy = -sum([i*math.log2(i) for i in Fre])

            pp = Fre.copy()
            pp.sort(reverse=True)

            temp = []
            num = 0
            for i in database:
                if pp.index(Fre[num]) < 10:
                    temp.append(f'{pp.index(Fre[num])}:{i}')
                num += 1
            # print(temp)  # ['7:远', '5:这', '1:一', '6:有', '8:他', '2:了', '9:罗', '4:是', '0:的', '3:不']
            top10 = [0,0,0,0,0,0,0,0,0,0]
            for i in temp:
                order = int(i[0])
                top10[order] = i[-1]
            top10 = ','.join(top10)
            record = str(len(database)) + ',' + top10 + ','+ str(entropy)[0:6] + '\n'


            print(record)
            with open(f'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Final_Results\{corpus}.txt','a') as f:
                f.write(record)


def Visualize():
    import pathlib
    import matplotlib.pyplot as plt
    import numpy as np
    path0 = r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\Final_Results'
    path1 = pathlib.Path(path0,'Biquge.txt')
    path2 = pathlib.Path(path0,'GuangMingRiBao.txt')
    path3 = pathlib.Path(path0,'English.txt')

    # Chinese
    data_1 = np.loadtxt(path1,dtype=str)
    data_2 = np.loadtxt(path2,dtype=str)

    entropy1 = [float(i[i.rfind(',')+1:]) for i in data_1]
    entropy2 = [float(i[i.rfind(',')+1:]) for i in data_2]


    fig,axes = plt.subplots()
    x_kedu = axes.get_xticklabels()
    [i.set_fontname('Times New Roman') for i in x_kedu]
    y_kedu = axes.get_yticklabels()
    [i.set_fontname('Times New Roman') for i in y_kedu]

    font1 = {'family':'Times New Roman','weight':'normal','size':20}
    x1 = np.arange(1,len(entropy1)+1)
    x2 = np.arange(1,len(entropy2)+1)
    plt.plot(x1,entropy1,linewidth = 3, label = 'Biquge',marker = '.',markersize = 15)
    plt.plot(x2,entropy2,linewidth = 3, label = 'GuangMingRiBao',marker = '.',markersize = 15)

    plt.xticks(range(1,51,5),range(2,101,10))
    plt.xlabel('Corpus Size(M)',font = font1)
    plt.ylabel('Entropy',font = font1)
    plt.tick_params(labelsize = 20)
    plt.legend(prop = font1)
    plt.show()


    # English
    data_3 = np.loadtxt(path3,dtype=str)
    entropy3 = [float(i[i.rfind(',')+1:]) for i in data_3]
    fig,axes = plt.subplots()
    x_kedu = axes.get_xticklabels()
    [i.set_fontname('Times New Roman') for i in x_kedu]
    y_kedu = axes.get_yticklabels()
    [i.set_fontname('Times New Roman') for i in y_kedu]

    font1 = {'family':'Times New Roman','weight':'normal','size':20}
    x3 = np.arange(1,len(entropy3)+1) # 671
    plt.plot(x3,entropy3,linewidth = 2.5, label = 'English',marker = '.',markersize = 6)

    plt.xticks(range(1,671+1,40),range(2,671*2+1,80))
    plt.xlabel('Corpus Size(M)',font = font1)
    plt.ylabel('Entropy',font = font1)
    plt.tick_params(labelsize = 20)
    plt.legend(prop = font1)
    plt.show()



def main():
    Visualize()
    a = HJW_Process()
    # a.English()
    a.Chinese('Biquge')
    a.Chinese('GuangMingRiBao')
    # a = GuangMingRiBao()
    # a.Create_FirstUrls()
    # a.Get_LastUrls()
    # a.Download()
    # a.pure()


    # a = Find_ChineseCorpus()
    # a.Create_DownloadUrl()
    # a.Downwords()

    # 下面是笔趣阁部分
    # a.GetBookUrls()
    # a.GetPageUrls()
    # a.DownloadBiquge()
    # a.pure()


    # a = Find_EnglishCorpus()
    # for i in range(8):
    #     a.Get_BookNum(a.cate_list[i],a.preurl_list[i],a.pages[i])
    # a.Get_Downloadpath(a.BookNum_dir)
    # a.AvoidSame()
    # a.Download_txt(r'D:\Vscode_Programming_Set\WebCrawler\English&Chinese_Corpus\AvoidSame_all.txt',a.BookSaved_dir)
    # a.Pure(a.BookSaved_dir)


main()