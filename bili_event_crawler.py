import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm.auto import tqdm
import re
import stanza
from collections import Counter
from tabulate import tabulate
from googletrans import Translator

print("\n비리비리 이벤트 페이지를 크롤링합니다...")

# 크롤링 전 세팅
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

chrome_options.add_argument("disable-gpu")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36")
# chrome_options.add_argument('headless')

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
# driver.maximize_window()

# 크롤링 URL
base_url = "https://www.bilibili.com/blackboard/activity-list.html?page="
n = 1

# 리스트 생성
text_lst=[]
date_lst = []
title_lst = []
status_lst =[]
detail_lst =[]
url_lst =[]
link_lst =[]

# 크롤링 시작
for f in range(110):
    url_path = base_url + str(n)
    wait = WebDriverWait(driver, 20)
    driver.get(url_path) 
    time.sleep(3)

    # 텍스트 가져오기    
    try:
        for text in tqdm(wait.until(EC.presence_of_all_elements_located((By.XPATH, '//*[@id="app"]/div/div[2]/ul/li')))): 
            if text.text != '':
                text_temp = text.text.replace('\n', ' ')
                if text_temp in text_lst:
                    continue
                text_lst.append(text_temp)
            else:
                continue
    except:
        # 크롤링 값이 없을 경우에
        # text_lst.append('')
        xyz = 0

    # url 가져오기
    try:
        for url in tqdm(wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'a')))): 
            if url.text != '':
                href = url.get_attribute('href')
                url_lst.append(href)
            else:
                url_lst.append(' ')         
    except:
        # 크롤링 값이 없을 경우에
        # url_lst.append('')
        xyz = 0

    # 링크 가져오기
    try :
        for i in url_lst:
            if "blackboard" in i:
                link_lst.append(i)
    except:
        link_lst.append('')

    link_lst = link_lst[:len(link_lst)-12]
    n+=1
    

if (1==1):
    # 제목 가져오기
    for title in text_lst :
        title_temp = title.split(' ')[0]
        title_lst.append(title_temp)

    # 상태 가져오기
    for status in text_lst :
        status_temp = status.split(' ')[1]
        status_lst.append(status_temp)

    # 기간 가져오기
    for date in text_lst :
        date_temp = date.split(' ')[2:5]
        date_lst.append(date_temp)


    # 설명 가져오기
    for detail in text_lst :
        detail_temp = detail.split(' ')[5:]
        detail_lst.append(detail_temp)


# 데이터프레임으로 변환
df = pd.DataFrame(
    {   '제목': title_lst,
        '상태': status_lst,
        '기간': date_lst,
        '설명': detail_lst,
        '링크': link_lst,
    })

# 인덱스 1부터 실행
df.index = df.index+1

# to_csv 저장
filename = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
name = input("저장할 파일명을 입력하세요 : ")
df.to_csv(name + " bili_huodong"+ " " + filename + ".csv" , encoding='utf-8-sig')


print('save done')
