# What to Wear
Repo:[https://github.com/lusteven901228/What-to-Wear](https://github.com/lusteven901228/What-to-Wear)
### 110-1 商管程式設計 第58組
展示影片：
[![展示影片](https://img.youtube.com/vi/JFuwuWfyNZo/maxresdefault.jpg)](https://youtu.be/JFuwuWfyNZo)

## Requirements
* python >=3.8 (3.9 used)
* kivy==2.0.0 (virtual environment recommended)
* requests (included in kivy)
* pandas (only crawler.py)
* selenium (only crawler.py)
* buildozer @ Linux/ macOS

## 創作理念

你是否在出門時，認為今日天氣晴朗而著短袖出門，但傍晚氣溫驟降，開始後悔出門時沒有多披件大衣？<br />
你又是否常常早上站在衣櫃前猶豫不決，不知道該穿什麼好？<br />
你會不會在買衣服時，卻又不知道那些單品符合現在溫度的需求？<br />
<br />
因此，本團隊製作了一個方便操作，易上手的APP，能夠根據當日的天氣預報，<br />
並在使用者提供性別，所在地區及顏色偏好後，輸出符合當日天氣狀況的穿搭範例，<br />
並提供市面上服裝的圖案範例，解決這類氣候狀況與溫度問題。<br />

## 程式說明

![程式邏輯圖解](https://i.imgur.com/He5SG3d.png)
* crawler.py: 資料庫擷取(爬蟲)
* allclothes.csv: 資料庫
* main.py: 前端執行檔
* main.kv: kivy需求
* buildozer.spec: 包裝config
### crawler.py

#### 創造一個FIFO的Queue, 放入所有的url
```python=18
q = Queue()
```
```python=23
    with open('HnMurls.txt','r') as f:
        while line:=f.readline():
            q.put(line)
```
#### 創造多個thread，並依輸入數量創造chromedriver(selenium)的worker
```python
    t = []  # list of threads
    for _ in range(thrs):
        t.append(Thread(target=HnM_Crawler_thread))  # Calling each target thread
        t[-1].start()
```
#### 其中，worker依序處理Queue中的url
```python
def HnM_Crawler_thread():
    driver = webdriver.Chrome()
    while not q.empty():
        HnM_Crawler(driver, q.get())
    driver.quit()
```
#### 透過網址分類，並使用query限制指定顏色、顯示圖片種類(原為模特兒->產品)、每頁顯示數量
```python
HnM_colors = {'brown': '咖啡色_a52a2a', 'turquoise': '土耳其藍_40e0d0', 'multiple': '多色_000000', 'orange': '橘色_ffa500', 'gray': '灰色_808080', 'white': '白色_ffffff', 'beige': '米色_f5f5dc', 'pink': '粉紅色_ffc0cb', 'red': '紅色_ff0000', 'purple': '紫色_800080', 'green': '綠色_008000', 'blue': '藍色_0000ff', 'gold': '金色_ffd700', 'silver': '銀色_c0c0c0', 'yellow': '黃色_ffff00', 'black': '黑色_000000', 'copper': '古銅色_cd7f32', 'clear': '透明_ffffff'}
HnM_default_query = '?sort=stock&image-size=small&image=stillLife&offset=0&page-size=5000&colorWithNames='
```
#### 爬蟲-1 透過網址標示標籤
```python
def HnM_Crawler(driver, url):
    info = url[url.find('zh_asia3')+9:-6].split('/')
```
#### 爬蟲-2
直接抓取圖片src/data-src
(經觀察後網站僅會讀取24張圖片，填入src attribute，其他則存在data-src attribute)
以append模式加入檔案內
```python
    for color, color_q in HnM_colors.items():
        driver.get(url+HnM_default_query+color_q)
        elements = driver.find_elements(By.XPATH, '//img[@class="item-image"]')
        for i in elements:
            pic_url = i.get_attribute('src') or ('https:'+i.get_attribute('data-src'))
            try:
                file_name = re.match(r'.+/(\w+\.jpg)',pic_url).group(1)
            except AttributeError:
                continue
            info2 = '\t'.join((file_name,pic_url,*info,color,i.get_attribute('alt'))) + '\n'
            open('HnM.csv','a',encoding='utf-8').write(info2)
```
#### 使用pandas篩選不符合格式之資料
```python
    df = pd.read_csv('HnM.csv', encoding='utf-8', delimiter='\t', on_bad_lines='skip')
    df.to_csv('allclothes.csv', encoding='utf-8',index=False)
```
### data_process.py
**因為讀到[這個issue](https://github.com/kivy/python-for-android/issues/2425)說pandas在apk包裝上有問題，且資料量不太大(~25000項)，故不使用pandas進行資料處理，以免衍伸更多麻煩**
利用csv module讀入檔案：
* allclothes.csv (衣服列表)
* men.csv, women.csv(手動標示男女裝合適溫度、穿著部位標示)
```python
import csv

# 開啟檔案
def open_csv(name):
    with open('%s.csv' % name, newline='', encoding="utf-8") as csvfile:
        file = []
        rows = csv.reader(csvfile)
        for row in rows:
            file.append(row)
    return 
```
#### 建立clothes的class，以property形式儲存個欄資料
#### 增加一個class method，為資料併入做準備
```python
class Clothes:    
    def __init__(self, lables):
        self.pic = lables[0]
        self.url = lables[1]
        self.gender = lables[2]
        self.label = lables[3]
        self.color = lables[4]
        self.name = lables[5]
    
    def add_ctype_and_temp(self, clist):
        temps = []
        label = self.label
        for types in clist:
            if label == types[0]:
                self.ctype = int(types[3])
                t = types[2].split(",")
                for i in range(len(t)):
                    t[i] = int(t[i])
                temps.append(t)
                self.temp = temps[0]
```
#### 將讀入的clothes存入一個list
```python
finallist = []      
for clothes in allclothesfl:
    clothes[3] = clothes[3] + clothes[4]    #label 2+3
    del clothes[4]
    if clothes[2] == 'ladies':
        if clothes[3] in OK_label_w:
            finallist.append(Clothes(clothes))
    if clothes[2] == 'men':
        if clothes[3] in OK_label_m:
            finallist.append(Clothes(clothes))        
del allclothesfl
```
#### 一一加入men, women的溫度、部位標示，
```python
for clothes in finallist:
    if clothes.gender == "ladies":
        clothes.add_ctype_and_temp(womenlst)
    elif clothes.gender == "men":
        clothes.add_ctype_and_temp(menlst)
```
#### 宣告篩選函式，篩選符合條件之資料
```python
def sieve(finallist, give_temp, give_color, give_gender):
    toplist = []
    bottomlist =[]
    outerlist = []
    shoeslist = []
    acclist = []
    #溫度轉編號
    if give_temp >= 19:
        if give_temp >= 27:
            if give_temp >= 31:
                temp_NO = 7
            else:
                temp_NO = 6
        elif give_temp > 23:
            temp_NO = 5
        else:
            temp_NO = 4
    elif give_temp > 11:
        if give_temp > 15:
            temp_NO = 3
        else:
            temp_NO = 2
    else:
        temp_NO = 1
    #開始過濾
    for x in finallist:
        if x.gender == give_gender:
            if x.color == give_color:   
                if temp_NO in x.temp:
                    if x.ctype == 1:
                        toplist.append(x)
                    elif x.ctype == 2:
                        bottomlist.append(x)
                    elif x.ctype == 3:
                        outerlist.append(x)
                    elif x.ctype == 4:
                        shoeslist.append(x)
                    elif x.ctype == 5:
                        acclist.append(x)
                    elif 1 in x.ctype and 2 in x.ctype:
                        toplist.append(x)
                        bottomlist.append(x)
                    elif 1 in x.ctype and 3 in x.ctype:
                        toplist.append(x)
                        outerlist.append(x)
    return(toplist, bottomlist, outerlist, shoeslist, acclist)
```
#### 分三個函式隨機選取衣服
特殊條件：全域變數
```python
bool_dresses = False
bool_shirts = False
```

* ran_bottom(下裝，若上裝圍裙子則不跑出來)
```python
def ran_bottom(alist, showobjectlst):
    if (not alist) or bool_dresses:
        showobjectlst.append(0)
        return 0
    i = random.randint(0,len(alist)-1)
    showobject = alist[i]
    showobjectlst.append(showobject)
    return showobject
```
* ran_outer(外套，若上衣為襯衫則外套不能為襯衫)
```python
def ran_outer(alist, showobjectlst):

    while alist:
        i = random.randint(0,len(alist)-1)
        showobject = alist.pop(i)

        if not "knitwear" in showobject.label and not (bool_shirts and "shirts" in showobject.label):
            showobjectlst.append(showobject)
            return showobject
    showobjectlst.append(0)
    return 0
```
* ran(其他，若為襯衫、裙子觸發條件則更改全域變數)
```python
def ran(alist, showobjectlst):
    global bool_dresses, bool_shirts
    
    while alist:
        i = random.randint(0,len(alist)-1)
        showobject = alist.pop(i)
        if not "knitwear" in showobject.label:
            if "dresses" in showobject.label:
                bool_dresses = True
            elif 'shirts' in showobject.label:
                bool_shirts = True
            showobjectlst.append(showobject)
            return showobject
    showobjectlst.append(0)
    return 0
```
#### 最後，建立主函式，將被import到其他檔案中
```python
def get_rand_combinations(give_gender, give_color, give_temp):
    global bool_dresses, bool_shirts
    bool_dresses, bool_shirts = False, False
    showobjectlst = []
    #過濾始符合前端條件並分部位
    afterlist = sieve(finallist, give_temp, give_color, give_gender)
    toplist = afterlist[0]
    bottomlist = afterlist[1] 
    outerlist = afterlist[2]
    shoeslist = afterlist[3]
    acclist = afterlist[4]
    ran(toplist, showobjectlst)
    ran_bottom(bottomlist, showobjectlst)
    ran_outer(outerlist, showobjectlst)
    ran(shoeslist, showobjectlst)
    ran(acclist, showobjectlst)
    allmatch_bottom = ('black', 'blue')
    allmatch_shoes = ('black', 'white', 'beige', 'gray')
    if not showobjectlst[1] and not bool_dresses:
        showobjectlst[1] = ran(sieve(finallist, give_temp, allmatch_bottom[random.randint(0,1)], give_gender)[1], showobjectlst[:])
    if not showobjectlst[0]:
        showobjectlst[0] = ran(sieve(finallist, give_temp, 'white', give_gender)[0], showobjectlst[:])
    if not showobjectlst[3]:
        showobjectlst[3] = ran(sieve(finallist, give_temp, allmatch_shoes[random.randint(0,3)], give_gender)[3], showobjectlst[:])
    return showobjectlst
```
### main.py UI主程式
#### 畫面一：SelectionScreen
首先畫出我們預計排版方式，並思考運用哪些Layout比較好

![第一頁UI](https://scontent-tpe1-1.xx.fbcdn.net/v/t39.30808-6/p843x403/270298463_1452235508531270_3390389977920589262_n.jpg?_nc_cat=101&ccb=1-5&_nc_sid=730e14&_nc_ohc=-CymUPvnHq4AX-x8wPg&_nc_ht=scontent-tpe1-1.xx&oh=00_AT9-JHS90SkXz7MIbi1sxR_6ANFLt_ckKKXfJYg16EUUbw&oe=61DB3DD1)
#### 依據排版格式寫出對應格式
#### kivy以此作為參照生成介面
```python
<SelectionScreen>:
    background_color: 1, 1, 1, 1  # 背景
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size

    SelectionScreenBoxLayout:  # 紅色BoxLayout
        orientation:'vertical'
        SelectionTitleBoxLayout:  # 綠色BoxLayout
            orientation:'horizontal'
            size_hint_y: .0825
            Label:
                text:'篩選'
                font_name: 'fonts/font1.ttf'
                color: 0 , 0 , 0 , 1
            Button:
                background_normal: 'images/refresh_normal.png'
                background_down: 'images/refresh_down.png'
                color: 0 , 0 , 0 , 1
                size_hint_x: 0.178
                on_release: root.reset()
        ScrollView:  # 淺藍色ScrollView
            SubGridLayout:  # 淺藍色GridLayout
                size_hint_y: None
                height: root.grid_height
                cols: 2
                spacing: 0, 20
                Label:
                    text:'服裝性別'
                    font_name: 'fonts/font1.ttf'
                    size_hint_y: None
                    height: root.gender_label_size
                    color: 0 , 0 , 0 , 1
                GenderDropDown:...  # BoxLayout(同紫色)
                Label:
                    text:'縣市'
                    font_name: 'fonts/font1.ttf'
                    size_hint_y: None
                    height:root.city_label_size
                    color: 0 , 0 , 0 , 1
                CityDropDown:...  # BoxLayout(同紫色)
                Label:
                    text:'鄉鎮市區'
                    font_name: 'fonts/font1.ttf'
                    size_hint_y: None
                    height:root.region_label_size
                    color: 0 , 0 , 0 , 1
                RegionDropDown:...  # 紫色BoxLayout
                Label:
                    text:'顏色'
                    font_name: 'fonts/font1.ttf'
                    size_hint_y: None
                    height:root.color_label_size
                    color: 0 , 0 , 0 , 1
                ColorDropDown:...  # BoxLayout(同紫色)
        Button:
            text:'送出'
            font_name: 'fonts/font1.ttf'
            background_normal: 'images/green_down.png'
            background_down: 'images/yellow_normal.png'
            color: 0 , 0 , 0 , 1
            size_hint_y: 0.1
            on_release:root.send()
```
**其中kivy內含的Dropdown會導致畫面重疊
因此我們透過調整高度與可視度(opacity)手動製作下拉式選單
而利用純python生成物件的方式也有試過，然而似乎無法有效調整高度**

以服裝性別的選單為例，透過```self.gender_expanded```的變數儲存開合狀態
每次收合時，確認是否會更改「送出」鈕狀態

kivy部分
```python
orientation:'lr-tb'
Button:
    text:root.gender_main_button_text
    background_normal: 'images/dropdown_normal.png'
    background_down: 'images/dropdown_down.png'
    font_name: 'fonts/font1.ttf'
    on_release: root.gender_toggle_expand(root.gender_main_button_text)
    size_hint_y: None
    height:100
Button:
    text:'男裝'
    font_name: 'fonts/font1.ttf'
    on_release: root.gender_toggle_expand('男裝', 'men')
    size_hint_y: None
    height:root.gender_button_size
    opacity: root.gender_button_opacity
Button:
    text:'女裝'
    font_name: 'fonts/font1.ttf'
    on_release: root.gender_toggle_expand('女裝', 'ladies')
    size_hint_y: None
    height: root.gender_button_size
    opacity: root.gender_button_opacity
Widget: #fill the rest of the canvas
```
python部分
```python
def gender_toggle_expand(self,text,result=''):
        self.gender_expanded = not self.gender_expanded
        if self.gender_expanded:
            self.gender_button_size = 100
            self.gender_button_opacity = 1
            self.gender_label_size = 300
            self.grid_height += 200
        else:
            self.gender_button_size = 0
            self.gender_button_opacity = 0
            self.gender_main_button_text = text
            self.gender_label_size = 100
            self.grid_height -= 200
            
            # 刷新送出按鈕狀態
            if text != '服裝性別':
                global gender_s, gender_r
                gender_s, gender_r= True, result
                self.send_enabled = all((gender_s, city_s, region_s, color_s))
```
**只有當四個選項都選擇之後才會送出**
送出會觸發：
* 選擇日期：<=9:00：當天；>9:00：隔天 
* API呼叫，計算平均溫度: 9, 12, 15, 18 四個時間
* 頁面跳轉
```python
def send(self):
        global today
        if not self.send_enabled:
            return None
        now = datetime.now()
        if now > now.replace(hour=9, minute=0, second=0, microsecond=0):
            now += timedelta(days=1)
            today = False
        else:
            today = True
        default_url = 'https://opendata.cwb.gov.tw/api/v1/rest/datastore/'
        params = {
            'Authorization':'CWB-DEA40550-C777-45A5-A771-2F6D01BCBCEE',
            'format':'JSON',
            'locationName':region_r,
            'elementName':'T',
            'sort':'time',
            'timeFrom': now.strftime('%Y-%m-%dT08:59:59'),
            'timeTo': now.strftime('%Y-%m-%dT21:00:01')
        }
        r = requests.get(default_url+city_r, params=params).json()
        global temperature, AavgT
        temperature = []
        for i in r['records']['locations'][0]['location'][0]['weatherElement'][0]['time']:
            temperature.append(int(i['elementValue'][0]['value']))
        AavgT = sum(temperature)/5
        self.manager.transition.direction = 'left'
        self.manager.current = 'result'
```

#### 第二頁：Result
![第二頁UI](https://i.imgur.com/iLYcpn8.jpg)

同樣框出Layout形式並撰寫對應kivy格式

```python
<ResultScreen>:
    background_color: 1, 1, 1, 1
    canvas:
        Color:
            rgba: 1, 1, 1, 1
        Rectangle:
            pos: self.pos
            size: self.size
    ResultScreenBoxLayout:
        orientation:'vertical'
        ResultScreenTitleBoxLayout: 
            orientation:'horizontal'
            size_hint_y: 0.075
            Button:
                background_normal: 'images/return_normal.png'
                background_down: 'images/return_down.png'
                color: 0 , 0 , 0 , 1
                size_hint_x: 0.162
                on_release: 
                    root.manager.transition.direction = 'right'
                    root.manager.current = 'selection'
            Label:
                text:'result'
                font_name: 'fonts/font1.ttf'
                color: 0 , 0 , 0 , 1
            Button:
                background_normal: 'images/refresh_normal.png'
                background_down: 'images/refresh_down.png'
                color: 0 , 0 , 0 , 1
                size_hint_x: 0.207
                on_release: root.refresh()
        ResultScreenStackLayout:
```
定義refresh函式在重刷時重新篩選並更新圖片
```python
def refresh(self):
    global getdata_result
    getdata_result = data_process.get_rand_combinations(gender_r, color_r, AavgT)
    if today:
        self.result_text = f'今天日間平均溫度:{AavgT:.1F}°C'
        print()
    else:
        self.result_text = f'明天日間平均溫度:{AavgT:.1F}°C'

    if len(getdata_result)>4:
        if getdata_result[0]:
            self.resultimagea = getdata_result[0].url
            self.resultlabela = getdata_result[0].name
            self.result_opacitya = 1
        else:
            self.resultimagea = 'images/na.png'
            self.resultlabela = '無'
            self.result_opacitya = 0

        if getdata_result[1]:
            self.resultimageb = getdata_result[1].url
            self.resultlabelb = getdata_result[1].name
            self.result_opacityb = 1
        else:
            self.resultimageb = 'images/na.png'
            self.resultlabelb = '無'
            self.result_opacityb = 0

        if getdata_result[2]:
            self.resultimagec = getdata_result[2].url
            self.resultlabelc = getdata_result[2].name
            self.result_opacityc = 1
        else:
            self.resultimagec = 'images/na.png'
            self.resultlabelc = '無'
            self.result_opacityc = 0

        if getdata_result[3]:
            self.resultimaged = getdata_result[3].url
            self.resultlabeld = getdata_result[3].name
            self.result_opacityd = 1
        else:
            self.resultimaged = 'images/na.png'
            self.resultlabeld = '無'
            self.result_opacityd = 0

        if getdata_result[4]:
            self.resultimagee = getdata_result[4].url
            self.resultlabele = getdata_result[4].name
            self.result_opacitye = 1
        else:
            self.resultimagee = 'images/na.png'
            self.resultlabele = '無'
            self.result_opacitye = 0
```
## Buildozer
進 Linux (我用 Ubuntu 20.04)
跟著documentation弄
用USB偵錯抓缺少的dependent

## References
* kivy documentation
* [kivy_tutorial](https://www.youtube.com/watch?v=l8Imtec4ReQ)
* stackoverflow (至少30篇)
* [buildozer](https://github.com/kivy/buildozer)
