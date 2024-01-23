import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
browser = webdriver.Chrome()
browser.maximize_window

#페이지 이동
url = 'https://finance.naver.com/sise/sise_market_sum.naver?&page='
browser.get(url)

time.sleep(3)

#조회항목초기화
checkboxes = browser.find_elements(By.NAME, 'fieldIds')
for checkbox in checkboxes:
    if checkbox.is_selected():
        checkbox.click()
time.sleep(3)  


#조회 항목 설정(원하는 항목)
items_to_select = ['영업이익', '자산총계', '매출액'] 
for checkbox in checkboxes:
    parent = checkbox.find_element(By.XPATH, '..')#부모 엘리먼트 찾기
    label = parent.find_element(By.TAG_NAME, 'label')
    #print(label.text)
    if label.text in items_to_select:
        checkbox.click()

time.sleep(3)     

#적용하기
btn_apply = browser.find_element(By.XPATH, '//a[@href="javascript:fieldSubmit()"]')
btn_apply.click()
time.sleep(10)
for idx in range(1,40): #1이상 40미만 페이지

    browser.get(url + str(idx))

    #5. 데이터 추출
    df = pd.read_html(browser.page_source)[1]
    df.dropna(axis='index', how='all',inplace=True)
    df.dropna(axis='columns', how='all',inplace=True)
    if len(df) == 0: 
        break
    time.sleep(10)

    #6 파일저장
    f_name = 'sise.csv'
    if os.path.exists(f_name):
        df.to_csv(f_name, encoding='utf-8-sig', index=False, mode='a', header=False)
    else:
        df.to_csv(f_name, encoding='utf-8-sig', index=False)
    print(f'{idx}페이지 완료')
    time.sleep(5)

browser.quit()