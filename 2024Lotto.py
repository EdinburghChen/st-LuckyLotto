import streamlit as st
import pandas as pd
import numpy as np

import datetime
import sqlite3
#from bs4 import BeautifulSoup
import requests
#import streamlit as st
#import pandas as pd
import random as rd

# 要發送的訊息
message = '\n💰幸運號碼:\n'
# LINE Notify 權杖
token = 'i77jiNSxnnmmyIEPzyynUjvSQtuUycRsVn4QU5D0BBI'

# 日期轉換格式->20170302
def convertDate(date):
    # 將日期文字字串轉換為日期物件
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    # 將日期物件轉換為 ISO8601 字符串
    iso8601_string = date.isoformat()
    return iso8601_string

# 設定網頁標題
st.title('小確幸')
# 加入網頁文字內容
st.write("今日小確幸")

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')

conn=sqlite3.connect("./pydb.db")

#st.write("最近一期獎號：")
try:
  # 建立資料庫連線 SQLite
  cursorLatest=conn.cursor()
  sqlQueryStrLatest="SELECT 球號,類型,日期 FROM L649 ORDER BY DATE(日期) DESC LIMIT 35;"
  cursorLatest.execute(sqlQueryStrLatest)
  #建立一個空串列用於存放結果
  LatestNo=[]

  for row in cursorLatest.fetchall():
      LatestNo.append(row[0])

  conn.commit()
  # Close the cursor and delete it
  cursorLatest.close()
  del cursorLatest
  #st.write("近期獎號：:red[" + str(LatestNo)+"]")

  for i in range(0, len(LatestNo),7):
    st.write(*LatestNo[i:i+7])  # 使用 * 運算子來解包串列，並用空格分隔

 
except Exception as e:
  st.write("Error: %s" % e)  


##

#表格
#df = pd.DataFrame(
#        np.random.randn(5, 6),
#        columns=('球號 %d' % i for i in range(6)))
# 互動式表格
#st.dataframe(df)
# 靜態表格
#st.table(df)
  
try:
  # 建立資料庫連線 SQLite
  #近5期1次以上
  cursor2=conn.cursor()
  sqlQueryStr="SELECT 球號, COUNT(球號) AS 計數 FROM L649 WHERE 日期 IN (SELECT 日期 FROM L649 GROUP BY 日期 ORDER BY DATE(日期) DESC LIMIT 5) GROUP BY 球號 HAVING 計數 >1 ORDER BY 計數 DESC"
  cursor2.execute(sqlQueryStr)

  #近5期所有號碼
  cursor3=conn.cursor()
  sqlQueryStr="SELECT 球號, COUNT(球號) AS 計數 FROM L649 WHERE 日期 IN (SELECT 日期 FROM L649 GROUP BY 日期 ORDER BY DATE(日期) DESC LIMIT 5) GROUP BY 球號  ORDER BY 計數 DESC"
  cursor3.execute(sqlQueryStr)


  #建立一個空串列用於存放結果
  #近5期1次以上
  issuedbigone=[]
  #近5期所有號碼
  issuedall=[]

  #建立一個1-49串列
  numbers = [str(x).zfill(2) for x in range(1, 50)]

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

  
  #已開出
  issued=issuedall
  #未開出
  unissued=numbers

  #網頁顯示資料
  #st.write("資料分析中")
  #st.write("STEP #2 Complete!!")
  st.write("A.近5期已開出獎號("+str(len(issued))+"/49):")
  st.write(str(issued))
  st.write("B.開出獎號>1次("+str(len(issuedbigone))+"/"+str(len(issued))+"):")
  st.write(":red["+str(issuedbigone)+"]")
  st.write("C.近5期未開出獎號("+str(len(unissued))+"/49):")
  st.write(str(unissued))

  if st.button('A7', type="primary"):
   #luckyNo
   luckyNo=rd.sample(issued, k=7)  #近5期
   #luckyNo2=rd.sample(numbers, k=1)
   #luckyNo.extend(luckyNo2)
   mA7=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mA7}
   # 以 requests 發送 POST 請求
   #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("A7:" + mA7)

  if st.button('A6C1', type="primary"):
   #luckyNo
   luckyNo=rd.sample(issued, k=6)  #近5期
   luckyNo2=rd.sample(numbers, k=1)
   luckyNo.extend(luckyNo2)
   mA6C1=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mA6C1}
   # 以 requests 發送 POST 請求
   #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("A6C1:" + mA6C1)

#   if st.button('A4C3', type="primary"):
#    #luckyNo
#    luckyNo=rd.sample(issued, k=4)  #近5期1次以上
#    luckyNo2=rd.sample(numbers, k=3)
#    luckyNo.extend(luckyNo2)
#    mA4C3=message+(str(luckyNo))
#    # HTTP 標頭參數與資料
#    headers = {"Authorization": "Bearer " + token}
#    data = {'message': mA4C3}
#    # 以 requests 發送 POST 請求
#    #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
#    st.write("A4C3:"+ mA4C3)

#   if st.button('B4C3', type="primary"):
#    #luckyNo
#    luckyNo=rd.sample(issuedbigone, k=4)  #近5期1次以上
#    luckyNo2=rd.sample(numbers, k=3)
#    luckyNo.extend(luckyNo2)
#    mB4C3=message+(str(luckyNo))
#    # HTTP 標頭參數與資料
#    headers = {"Authorization": "Bearer " + token}
#    data = {'message': mB4C3}
#    # 以 requests 發送 POST 請求
#    #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
#    st.write("B4C3:" + mB4C3)

#   if st.button('B3C4', type="primary"):
#    #luckyNo
#    luckyNo=rd.sample(issuedbigone, k=3)  #近5期1次以上
#    luckyNo2=rd.sample(numbers, k=4)
#    luckyNo.extend(luckyNo2)
#    mB3C4=message+(str(luckyNo))
#    # HTTP 標頭參數與資料
#    headers = {"Authorization": "Bearer " + token}
#    data = {'message': mB3C4}
#    # 以 requests 發送 POST 請求
#    #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
#    st.write("B3C4:" + mB3C4)

  if st.button('B2C5', type="primary"):
   #luckyNo
   luckyNo=rd.sample(issuedbigone, k=2)  #近5期1次以上
   luckyNo2=rd.sample(numbers, k=5)
   luckyNo.extend(luckyNo2)
   mB2C5=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mB2C5}
   # 以 requests 發送 POST 請求
   #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("B2C5:" + mB2C5)

  if st.button('C1', type="primary"):
   #luckyNo
   luckyNo=rd.sample(numbers, k=1)
   mC1=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mC1}
   # 以 requests 發送 POST 請求
   #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("C1:" + mC1)   

  if st.button('C7', type="primary"):
   #luckyNo
   luckyNo=rd.sample(numbers, k=7)
   mC7=message+(str(luckyNo))
   # HTTP 標頭參數與資料
   headers = {"Authorization": "Bearer " + token}
   data = {'message': mC7}
   # 以 requests 發送 POST 請求
   #requests.post("https://notify-api.line.me/api/notify",headers=headers, data=data)
   st.write("C7:" + mC7)  

except Exception as e:
  st.write("Error: %s" % e)

st.divider()
#inputdate=st.date_input('獎號日期',datetime.date(2024, 2, 29))
inputdate=st.date_input('獎號日期',datetime.date.today())
data_Info_Dict = (st.text_input('請輸入號碼')).split(',')
st.write('輸入號碼:', *data_Info_Dict)
if st.button('新增獎號', type="primary"):
   #st.write('新增獎號：'+ inputdate.strftime('%Y-%m-%d')+data_Info_Dict)  
  #新增--
   try:
     # 建立資料庫連線 SQLite
     cursor=conn.cursor()
     sqlstr="CREATE TABLE IF NOT EXISTS L649 ('球號' TEXT NOT NULL, '類型' TEXT NOT NULL, '日期' TEXT NOT NULL,PRIMARY KEY('球號','類型','日期'));"
     cursor.execute(sqlstr)

     for  i in range(len(data_Info_Dict)):
       print (data_Info_Dict[i])
       if (i >= 0):
          # Prepare the stored procedure execution script and parameter values
          sqlIns="INSERT OR IGNORE INTO L649 ('球號','類型','日期')  VALUES(?,?,?)"
          for index, LNO in enumerate(data_Info_Dict):
              if (index == 6):
                cursor.execute(sqlIns,(LNO,'S',convertDate(inputdate.strftime('%Y-%m-%d')))) 
                conn.commit()
                #print(sqlIns + "('"+LNO+ "','S','"+convertDate(mydate)+"')")
              else:
                cursor.execute(sqlIns,(LNO,'N',convertDate(inputdate.strftime('%Y-%m-%d')))) 
                conn.commit() 
   except Exception as e:
     print("Error: %s" % e) 

   # Close the cursor and delete it
   cursor.close()
   del cursor 



  #---

st.divider()
if st.button('清空資料庫', type="primary"):
   try:
      # 建立資料庫連線 SQLite
     cursor=conn.cursor()
     sqlstr="DELETE FROM L649 WHERE 日期 = '"+ convertDate(inputdate.strftime('%Y-%m-%d')) +"';"
     cursor.execute(sqlstr)
     conn.commit()
     cursor.close()
     del cursor 
   except Exception as e:
      print("Error: %s" % e) 
   st.write('資料清除'+convertDate(inputdate.strftime('%Y-%m-%d')))  

#Close the database connection
conn.close() 
