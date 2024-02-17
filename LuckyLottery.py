import logging
import requests
import utils
import sqlite3
import streamlit as st
import random as rd

conn=sqlite3.connect("./pydb.db")
# 要發送的訊息
message = '\n💰幸運號碼:\n'

# LINE Notify 權杖
token = 'i77jiNSxnnmmyIEPzyynUjvSQtuUycRsVn4QU5D0BBI'

class LucasTaiwanLottery():
    NO_DATA = '查無資料'
    BASE_URL = 'https://api.taiwanlottery.com/TLCAPIWeB/Lottery'
    COUNT_OF_GROUP_1 = 6
    

    def get_lottery_result(self, url):
        response = requests.get(url)
        return response.json() 

    # 取得目前月份
    def get_current_month():
        return datetime.datetime.now().strftime('%m')

    # 取得目前年
    def get_current_year():
        return datetime.datetime.now().strftime('%Y')
    
    def SQliteIns649(T開獎日期,T獎號資訊):
      try:
       # 建立資料庫連線 SQLite
       cursor=conn.cursor()
       sqlstr="CREATE TABLE IF NOT EXISTS L649 ('球號' TEXT NOT NULL, '類型' TEXT NOT NULL, '日期' TEXT NOT NULL,PRIMARY KEY('球號','類型','日期'));"
       cursor.execute(sqlstr)
    
       for  i in range(len(T獎號資訊)):
         if (i >= 0):
           # Prepare the stored procedure execution script and parameter values
           sqlIns="INSERT OR IGNORE INTO L649 ('球號','類型','日期')  VALUES(?,?,?)"
           for index, LNO in enumerate(T獎號資訊):
             #輸出補零
             SLNO=(str) (LNO).zfill(2)
             if (index == 6):
               cursor.execute(sqlIns,(SLNO,'S',T開獎日期))
               conn.commit()
             else:
               cursor.execute(sqlIns,(SLNO,'N',T開獎日期))
               conn.commit()

      except Exception as e:
        print("Error: %s" % e) 

      #Close the cursor and delete it
      cursor.close()
      del cursor 

      return

    # 大樂透
    def lotto649(self, back_time=[utils.get_current_year(), utils.get_current_month()]):
        URL = "{}/Lotto649Result?period&month={}-{}&pageSize=31".format(self.BASE_URL, back_time[0], back_time[1])
       

        title = '大樂透_' + str(back_time[0]) + '_' + str(back_time[1])
        result = self.get_lottery_result(URL)
        total_size = result['content']['totalSize']
        lotto649_result = result['content']['lotto649Res']
        datas = []
        
        for i in range(total_size):
          #開獎日期
          my開獎日期=lotto649_result[i]['lotteryDate']
          my獎號資訊=lotto649_result[i]['drawNumberSize'][0:7]

          LucasTaiwanLottery.SQliteIns649(my開獎日期, my獎號資訊)


        for i in range(total_size):
            datas.append({
            "期別": lotto649_result[i]['period'],
            "開獎日期": lotto649_result[i]['lotteryDate'],
            "獎號": lotto649_result[i]['drawNumberSize'][0:self.COUNT_OF_GROUP_1],
            "特別號": lotto649_result[i]['drawNumberSize'][self.COUNT_OF_GROUP_1]
            })

        if len(datas) == 0:
         logging.warning(self.NO_DATA + title)

        return datas




# 設定網頁標題
st.title('大樂透小確幸')
# 加入網頁文字內容

lottery = LucasTaiwanLottery()
result = lottery.lotto649()

#近期獎號
for i in range(3):
  print(f"期別：{result[i]['期別']}")
  st.write(f"期別：{result[i]['期別']}，獎號：{result[i]['獎號']}[{result[i] ['特別號']}]")


  
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
   
except Exception as e:
  st.write("Error: %s" % e)


st.divider()
#inputdate=st.date_input('獎號日期',datetime.date(2024, 1, 1))
inputdate=st.date_input('開獎日期',datetime.date.today())
if st.button('同步開獎資料', type="primary"):
   st.write(inputdate)
   lottery.BASE_URL= 'https://api.taiwanlottery.com/TLCAPIWeB/Lottery'
   lottery.lotto649([inputdate.year,inputdate.month])
