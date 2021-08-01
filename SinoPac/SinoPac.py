import requests
import time
from lxml import html
from bs4 import BeautifulSoup as bs
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

LOGIN_ID='___' #身分證
LOGIN_PWD='___' #密碼
START_DATE= '2019-01-01' #yyyy-MM-dd
END_DATE= '2021-07-31' #yyyy-MM-dd
saveLocation = 'K:/研究報告/' #儲存位置

options = Options()
options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
browser = webdriver.Chrome(chrome_options=options, executable_path="C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe", )
browser.maximize_window()  # 最大化視窗
wait = WebDriverWait(browser, 2) # 等待載入2s

class wait_page_load:
    def __init__(self, browser, timeout=10):
        self.browser = browser
        self.timeout = timeout
        
    def __enter__(self):
        self.old_page = self.browser.find_element_by_tag_name('html')
        print(f'Old page id is {self.old_page.id}')
    
    def __exit__(self, *_):
        start = time.time()
        while time.time() - start < self.timeout:
            new_page = self.browser.find_element_by_tag_name('html')
            print(f'New page id is {new_page.id}')
            if new_page.id != self.old_page.id:
                return True
            else:
                time.sleep(1)
        raise Exception(f'Timeout after {self.timeout} secends')


def login():
    browser.get('https://scmreport2.sinotrade.com.tw/Report/Report_1/Report_11_1_10')
    iframe = browser.find_element_by_class_name('iframe')
    browser.switch_to.frame(iframe)
    idno = browser.find_element_by_id("idno")
    idno.send_keys(LOGIN_ID)
    pwd = browser.find_element_by_id("pwd")
    pwd.send_keys(LOGIN_PWD)
    
    submit = browser.find_element_by_class_name("cls_Submit")
    submit.click() 
    time.sleep(5)
    get_page_index()

def get_page_index():
    browser.get('https://scmreport2.sinotrade.com.tw/Report/Report_1/Report_11_1_10?ticker=&sdate='+START_DATE+'&edate='+END_DATE+'&pagesize=5000&page=1')
#     try:
#         print(browser.page_source)  # 輸出網頁原始碼
#     except Exception as e:
#         print(str(e))
    
login()

soup = bs(browser.page_source, 'html.parser')
data = []
for tr in soup.select('.table_1 tr'):
    td = tr.find('td')
    if (td != None):
        a = tr.find('a')
        downloadFileName = td.text.replace('-','') + '_' + a.text.replace('\t','').replace('/','').replace('，',' ').strip()+'.pdf';
        downloadUrl = 'https://scmreport2.sinotrade.com.tw/'+a.get('href')
        r = requests.get(downloadUrl)
        with open(saveLocation+downloadFileName,'wb') as f:
          f.write(r.content)
        print(saveLocation+downloadFileName+'下載成功')
    
    
    

