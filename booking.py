from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import smtplib
from email.mime.text import MIMEText as text
import time

def sendEmail(current_url):
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    smtpObj.starttls()
    smtpObj.login('jeremy455576@gmail.com', 'abcd6799') #第一個參數是電郵帳號，第二個參數是密碼

    m = text("NTU Hospital eye department can be booked now\n" + current_url)
    m['Subject'] = 'NTU Hospital Booking Infrom!'
    m['From'] = "jeremy455576@gmail.com"
    m['To'] = "jeremy4555@yahoo.com.tw"

    smtpObj.sendmail(m['From'], m['To'], m.as_string())

while True:
    url = "https://reg.ntuh.gov.tw/webadministration/DoctorServiceQueryByDrName.aspx?HospCode=T0&QueryName=林昭文"
    # url = 'https://reg.ntuh.gov.tw/webadministration/DoctorServiceQueryByDrName.aspx?HospCode=T0&QueryName=陳'

    driver = webdriver.Chrome()
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')[2]
    df = pd.read_html(str(table))[0]
    df.columns = df.loc[0]
    df.drop(0, inplace=True)
    df_notFull = df.loc[df['科別']=='眼科部'].loc[df['門診名稱']=='普通門診'].loc[df['掛號']=='.掛號.']
    isFull = len(df_notFull)
    if isFull != 0:
        indices = [idx+1 for idx in df_notFull.index]
        elem_id = "DoctorServiceListInSeveralDaysInput_GridViewDoctorServiceList__ctl" + str(indices[0]) + "_AdminTextShow"
        elem = driver.find_element_by_id(elem_id)
        driver.execute_script("arguments[0].click();", elem)
        current_url = driver.current_url
        sendEmail(current_url)

    else:
        print('Fail Booking!')
        
    driver.close()
    time.sleep(5)
    