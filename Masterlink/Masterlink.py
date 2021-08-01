import requests
from datetime import datetime
from lxml import html
from bs4 import BeautifulSoup as bs

saveLocation = './' #研究報告要儲存的資料夾
start_year=2019 #要抓的研究報告起始年度
end_year=2021 #要抓的研究報告結束年度
start_month=1 #要抓的研究報告起始月份
end_month=12 #要抓的研究報告結束月份
LOGIN_ID='___' #帳號(身分證)
LOGIN_TOKEN='___' #元富加密後的密碼(token)，請使用瀏覽器工具或Postman抓取

LOGIN_URL = 'https://mlec.masterlink.com.tw/amserver/UI/Login'
session_requests = requests.session()
result = session_requests.get(LOGIN_URL)

headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Upgrade-Insecure-Requests': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
}

payload = {
    'IDToken1': LOGIN_ID,
    'IDToken2': LOGIN_TOKEN,
    'ReturnURL': 'https://www.masterlink.com.tw/index.aspx',
    'goto': 'https://www.masterlink.com.tw/index.aspx'
}
# 登入
result = session_requests.post(LOGIN_URL, data=payload, headers=headers)

headers = {
    'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
    'sec-ch-ua-mobile': '?0',
    'Content-Type': 'text/plain;charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
    'Accept': '*/*'
}
inlineUrl = 'https://www.masterlink.com.tw/stock/investment_consulting/industry_study/XhrServices.aspx'

# 取得某年月的報告頁數
def getPageCount(year, month):
    pageCount = 0
    try:
        payload = payload = f'''<Paras>
                <UID>1000</UID>
                <SID>10000000</SID>
                <Subsite>2</Subsite>
                <FormID>1</FormID>
                <SystemID>1</SystemID>
                <Opr>L,WebPageL000007</Opr>
                <Idx>001</Idx><Conditions>
                <dataType>A</dataType>
                <year>{year}</year>
                <month>{month}</month>
                <topRecs>5</topRecs>
                <pageNo>1</pageNo>
                </Conditions>
                <RepTag>BkJobs</RepTag>
            </Paras>'''
        result = session_requests.post(inlineUrl, data=payload, headers=headers)
        # 多出來<![CDATA[ 所以無法解析
        soup = bs(result.text.replace('<![CDATA[', ''), 'html.parser')
        pageList = soup.select('.pageswitcher .page')
        pageCount = pageList[len(pageList)-1].text
        print(f'Year={year}, Month={month}, PageCount={pageCount}')
    except:
        print(f'Year={year}, Month={month}, No Data')
    return pageCount

for idx_Y in range(start_year, end_year+1):
    for idx_M in range(start_montg, end_month+1):
        pageCount = getPageCount(idx_Y, idx_M)
        for idx_P in range(0,int(pageCount)):
            payload = f'''<Paras>
                <UID>1000</UID>
                <SID>10000000</SID>
                <Subsite>2</Subsite>
                <FormID>1</FormID>
                <SystemID>1</SystemID>
                <Opr>L,WebPageL000007</Opr>
                <Idx>001</Idx><Conditions>
                <dataType>A</dataType>
                <year>{idx_Y}</year>
                <month>{idx_M}</month>
                <topRecs>5</topRecs>
                <pageNo>{idx_P+1}</pageNo>
                </Conditions>
                <RepTag>BkJobs</RepTag>
            </Paras>'''
            result = session_requests.post(inlineUrl, data=payload, headers=headers)
            # 多出來<![CDATA[ 所以無法解析
            soup = bs(result.text.replace('<![CDATA[', ''), 'html.parser')
            for link in soup.select('.tdContent a'):
                herf = link.get('href')
                items = herf[26:len(herf)-2].replace(chr(39),'').split(',')
                downloadUrl = 'https://www.masterlink.com.tw/DownloadFile.aspx?filename='+items[8]+'&linkSource='+items[0]
                dateStr = datetime.strptime(items[4], "%Y/%m/%d").strftime("%Y%m%d")
                downloadFileName = dateStr+'_'+items[2].replace('*','_')+'.pdf'

                r = requests.get(downloadUrl)
                with open(saveLocation+downloadFileName,'wb') as f:
                  f.write(r.content)
                print(saveLocation+downloadFileName+'下載成功')
