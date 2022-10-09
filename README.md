# django-multi-tenant-tutorial
## 全能住宅改造王，Django 多租戶架構的應用 —— 實作一個電商網站
### 前言

每次只要看到新的技術分享、新的專案作品、總是既興奮又期待，心中的聲音屢次衝擊著大腦『 這個技術好有趣！我也想試試看！』

從剛入行就持續著看一篇篇的技術文章。這次，就換我來分享給大家吧！

### 主題

『全能住宅改造王，Django 多租戶架構的應用 —— 實作一個電商網站』

一次開發一個專案並不困難，但一次開發五個大同小異的專案（產品）呢？要面對的不只是許多重複的環境建置、程式開發，還有版控管理、錯誤修復、版本升級、不同的客製需求等等。

多租戶架構是能解決上述問題的方案之一，不同的租戶之間可以共享相同的系統核心或是應用程式，同時又確保資料隔離。可彈性的調整租戶共享資源與獨享資源。系統核心升級也因為共享著核心而可以一次將全部租戶升級。

本次將會以多租戶架構為核心，Django 為工具，從認識多租戶架構與 Django 帶領大家入門，建立 Docker 容器化開發環境，逐步帶大家解決開發多租戶架構時會遇到的問題，將實務上會遇到的問題逐一擊破，手把手帶你一起打造一套多租戶架構的電商網站！

### 大綱

[Day 1  全能住宅改造王，Django 多租戶架構的應用 —— 實作一個電商網站](https://ithelp.ithome.com.tw/articles/10289335)  
[Day 2  多租戶架構好吃嗎？能給我多少好處？](https://ithelp.ithome.com.tw/articles/10289848)  
[Day 3  Django ？我很好奇！](https://ithelp.ithome.com.tw/articles/10290584)  
[Day 4  建立地基！使用 Docker](https://ithelp.ithome.com.tw/articles/10291255)  
[Day 5  蓋一棟 Django 小屋](https://ithelp.ithome.com.tw/articles/10292250)  
[Day 6  設計格局，Django 多租戶架構](https://ithelp.ithome.com.tw/articles/10292926)  
[Day 7  第一個房客，建立租戶](https://ithelp.ithome.com.tw/articles/10293755)  
[Day 8  認識模型，常用欄位與參數介紹](https://ithelp.ithome.com.tw/articles/10294473)  
[Day 9  模型要買櫃，實作 Model 模型](https://ithelp.ithome.com.tw/articles/10295259)  
[Day 10 Django Admin，管理室不收管理費](https://ithelp.ithome.com.tw/articles/10295952)  
[Day 11 ModelAdmin，成為一名模型管理員](https://ithelp.ithome.com.tw/articles/10296933)  
[Day 12 居家上班要懂的 Django 工作流程](https://ithelp.ithome.com.tw/articles/10297626)  
[Day 13 打造大廳，動手開發你的首頁](https://ithelp.ithome.com.tw/articles/10298086)  
[Day 14 貼上照片牆，Django 多租戶圖片上傳](https://ithelp.ithome.com.tw/articles/10299243)   
[Day 15 裝潢大廳，套用 Template 版面](https://ithelp.ithome.com.tw/articles/10299701)  
[Day 16 佈置房間， 將資料傳入 Template](https://ithelp.ithome.com.tw/articles/10300017)  
[Day 17 個人化，Django 多租戶網站設定](https://ithelp.ithome.com.tw/articles/10301230)  
[Day 18 個性風格，自定義樣式版面](https://ithelp.ithome.com.tw/articles/10301821)  
[Day 19 邁向國際化，Django 多語系](https://ithelp.ithome.com.tw/articles/10302174)  
[Day 20 搭上國際航空，切換語系](https://ithelp.ithome.com.tw/articles/10303094)  
[Day 21 國際化租屋，Django 多租戶多語系](https://ithelp.ithome.com.tw/articles/10303501)   
[Day 22 郵差來送信，使用 Django 寄送郵件](https://ithelp.ithome.com.tw/articles/10304202)  
[Day 23 使命必達！Django 多租戶下的任務排程](https://ithelp.ithome.com.tw/articles/10304728)  
[Day 24 裝上引擎，Django 的移動城堡](https://ithelp.ithome.com.tw/articles/10304743)  
[Day 25 改造引擎，Django 多租戶下的搜尋引擎](https://ithelp.ithome.com.tw/articles/10305671)  
[Day 26 Django 來找查，實作搜尋功能](https://ithelp.ithome.com.tw/articles/10306174)
[Day 27 合法克隆，複製你的 Django 租戶](https://ithelp.ithome.com.tw/articles/10306470)  

Github 若當日有更新程式會新增一個 branch，連結如下：   
https://github.com/ivanjo39191/django-multi-tenant-tutorial/

### 明日預告

明天將會開始介紹『多租戶架構好吃嗎？能給我多少好處？』。