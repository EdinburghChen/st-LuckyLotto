import datetime
import sqlite3
from bs4 import BeautifulSoup
import requests
import streamlit as st
import pandas as pd
import random as rd

# LINE Notify 權杖
token = 'i77jiNSxnnmmyIEPzyynUjvSQtuUycRsVn4QU5D0BBI'

# 要發送的訊息
message = '\n💰幸運號碼:\n'

# 設定網頁標題
st.title('今彩539小確幸')
# 加入網頁文字內容
#st.write("今日小確幸")

conn=sqlite3.connect("./pydb.db")


 # 球號
winning_Numbers_Sort_lotto = ['D539Control_history1_dlQuery_SNo1_', 'D539Control_history1_dlQuery_SNo2_', 'D539Control_history1_dlQuery_SNo3_',
                              'D539Control_history1_dlQuery_SNo4_', 'D539Control_history1_dlQuery_SNo5_']


def search_winning_numbers(css_class):
    global winning_Numbers_Sort_lotto
    if (css_class != None):
        for i in range(len(winning_Numbers_Sort_lotto)):
            if winning_Numbers_Sort_lotto[i] in css_class:
                return css_class


# 開獎日期
winning_Numbers_Date_lotto = ['D539Control_history1_dlQuery_D539_DDate_0', 'D539Control_history1_dlQuery_D539_DDate_1', 'D539Control_history1_dlQuery_D539_DDate_2',
                              'D539Control_history1_dlQuery_D539_DDate_3', 'D539Control_history1_dlQuery_D539_DDate_4', 'D539Control_history1_dlQuery_D539_DDate_5',
                              'D539Control_history1_dlQuery_D539_DDate_6', 'D539Control_history1_dlQuery_D539_DDate_7', 'D539Control_history1_dlQuery_D539_DDate_8',
                              'D539Control_history1_dlQuery_D539_DDate_9']


def search_winning_numbers_date(css_class):
    global winning_Numbers_Date_lotto
    if (css_class != None):
        for i in range(len(winning_Numbers_Date_lotto)):
            if winning_Numbers_Date_lotto[i] in css_class:
                return css_class


def parse_tw_lotto_html(data_Info, number_count):
    data_Info_List = []
    data_Info_Dict = {}
    tmp_index = 0
    for index in range(len(data_Info)):
        if (index == 0):
            data_Info_List.append(data_Info[index].text)
        else:
            if (index % number_count != 0):
                data_Info_List.append(data_Info[index].text)
            else:
                data_Info_Dict[str(tmp_index)] = list(data_Info_List)
                data_Info_List = []
                data_Info_List.append(data_Info[index].text)
                tmp_index = tmp_index+1
        data_Info_Dict[str(tmp_index)] = list(data_Info_List)
    return data_Info_List, data_Info_Dict


head_Html_lotto = 'https://www.taiwanlottery.com.tw/lotto/dailycash/history.aspx'
res = requests.get(head_Html_lotto, timeout=30)
soup = BeautifulSoup(res.text, 'lxml')

# 球號
header_Info = soup.find_all(id=search_winning_numbers)
data_Info_List, data_Info_Dict = parse_tw_lotto_html(header_Info, 5)  # 5筆1組

# 開獎日期
header_Info_date = soup.find_all(id=search_winning_numbers_date)
data_Info_List_Date, data_Info_Dict_Date = parse_tw_lotto_html(
    header_Info_date, 1)  # 1筆1組

# 日期轉換格式民國日期為西元:106/03/02->20170302
def convertDate(date):
    str1 = str(date)
    yearstr = str1[:3]  # 取出民國年
    realyear = str(int(yearstr) + 1911)  # 轉為西元年
    realdate = realyear + "-" + str1[4:6] + "-" + str1[7:9]  # 組合日期
    # 將日期文字字串轉換為日期物件
    date = datetime.datetime.strptime(realdate, '%Y-%m-%d')
    # 將日期物件轉換為 ISO8601 字符串
    iso8601_string = date.isoformat()
    return iso8601_string


try:
# 建立資料庫連線 SQLite
  cursor=conn.cursor()
  sqlstr="CREATE TABLE IF NOT EXISTS L539 ('球號' TEXT NOT NULL,  '日期' TEXT NOT NULL,PRIMARY KEY('球號','日期'));"
  #sqlstr="CREATE TABLE IF NOT EXISTS L649 ( 球號 TEXT NOT NULL, 類型 TEXT NOT NULL, 日期 TEXT NOT NULL);"
  cursor.execute(sqlstr)

  for i in range(len(data_Info_Dict)):
    mylistDate = data_Info_Dict_Date.pop(str(i))
    mydate = mylistDate[0]
    if (i >= 0):
       mylist = data_Info_Dict.pop(str(i))
       # Prepare the stored procedure execution script and parameter values
       sqlIns="INSERT OR IGNORE INTO L539 ('球號','日期')  VALUES(?,?)"
       for index, LNO in enumerate(mylist):
         if (index == 6):
           cursor.execute(sqlIns,(LNO,convertDate(mydate))) 
           conn.commit()
           #print(sqlIns + "('"+LNO+ "','S','"+convertDate(mydate)+"')")
         else:
           cursor.execute(sqlIns,(LNO,convertDate(mydate))) 
           conn.commit() 
except Exception as e:
  print("Error: %s" % e)
# Close the cursor and delete it
cursor.close()
del cursor
#Close the database connection
#conn.close() 
# 加入網頁文字內容
st.write("台灣彩券擷取資料中...")
#st.write("STEP #1 Complete!!")

try:
  # 建立資料庫連線 SQLite
  cursorLatest=conn.cursor()
  sqlQueryStrLatest="SELECT 球號,日期 FROM L539 ORDER BY DATE(日期) DESC LIMIT 5;"
  cursorLatest.execute(sqlQueryStrLatest)
  #建立一個空串列用於存放結果
  LatestNo=[]

  for row in cursorLatest.fetchall():
      LatestNo.append(row[0])

  conn.commit()
  # Close the cursor and delete it
  cursorLatest.close()
  del cursorLatest
  st.write("近期獎號：:red[" + str(LatestNo)+"]")

except Exception as e:
  st.write("Error: %s" % e)  


try:
  # 建立資料庫連線 SQLite
  #近5期1次以上
  cursor2=conn.cursor()
  sqlQueryStr="SELECT 球號, COUNT(球號) AS 計數 FROM L539 WHERE 日期 IN (SELECT 日期 FROM L539 GROUP BY 日期 ORDER BY DATE(日期) DESC LIMIT 6) GROUP BY 球號 HAVING 計數 >1 ORDER BY 計數 DESC"
  cursor2.execute(sqlQueryStr)

  #近5期所有號碼
  cursor3=conn.cursor()
  sqlQueryStr="SELECT 球號, COUNT(球號) AS 計數 FROM L539 WHERE 日期 IN (SELECT 日期 FROM L539 GROUP BY 日期 ORDER BY DATE(日期) DESC LIMIT 6) GROUP BY 球號  ORDER BY 計數 DESC"
  cursor3.execute(sqlQueryStr)


  #建立一個空串列用於存放結果
  #近6期1次以上
  issuedbigone=[]
  #近5期所有號碼
  issuedall=[]

  #建立一個1-39串列
  numbers = [str(x).zfill(2) for x in range(1,40)]

  #將查詢結果逐一加入串列
  #近5期1次以上
  for row in cursor2.fetchall():
      issuedbigone.append(row[0])
      #numbers.remove(row[0])

 #將查詢結果逐一加入串列
  for row in cursor3.fetchall():
      issuedall.append(row[0])
      numbers.remove(row[0])
  
  conn.commit()
  # Close the cursor and delete it
  cursor2.close()
  cursor3.close()
  del cursor2
  del cursor3
  #Close the database connection
  conn.close() 
  
  #已開出
  issued=issuedall
  #未開出
  unissued=numbers

  #網頁顯示資料
  #st.write("資料分析中")
  #st.write("STEP #2 Complete!!")
  st.write("A.近6期已開出獎號("+str(len(issued))+"/39):")
  st.write(str(issued))
  st.write("B.開出獎號>1次("+str(len(issuedbigone))+"/"+str(len(issued))+"):")
  st.write(":red["+str(issuedbigone)+"]")
  st.write("C.近6期未開出獎號("+str(len(unissued))+"/39):")
  st.write(str(unissued))

  if st.button('A6', type="primary"):
   #luckyNo
   luckyNo=rd.sample(issued, k=6)  #近5期
   #luckyNo2=rd.sample(numbers, k=1)
   #luckyNo.extend(luckyNo2)
   mA6=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mA6}
   # 以 requests 發送 POST 請求
   requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("A6:" + mA6)

  if st.button('A5C1', type="primary"):
   #luckyNo
   luckyNo=rd.sample(issued, k=5)  #近5期
   luckyNo2=rd.sample(numbers, k=1)
   luckyNo.extend(luckyNo2)
   mA5C1=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mA5C1}
   # 以 requests 發送 POST 請求
   requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("A6C1:" + mA5C1)


  if st.button('C1', type="primary"):
   #luckyNo
   luckyNo=rd.sample(numbers, k=1)
   mC1=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mC1}
   # 以 requests 發送 POST 請求
   requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("C1:" + mC1)   
   
except Exception as e:
  st.write("Error: %s" % e)
