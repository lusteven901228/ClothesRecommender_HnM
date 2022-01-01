from kivy.app import App
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.uix.stacklayout import StackLayout
from datetime import datetime, timedelta
import requests
import data_process

Builder.load_string(open('main.kv','r',encoding='utf-8').read())

gender_s = False
gender_r = ''
city_s = False
city_r = ''
region_s = False
region_r = ''
color_s = False
color_r = ''
temperature = []
getdata_result = []
today = True
AavgT = 0

class SelectionScreen(Screen):
    send_enabled = False
    gender_main_button_text = StringProperty('服裝性別')
    gender_expanded = False
    gender_button_size = NumericProperty(0)
    gender_button_opacity = NumericProperty(0)
    gender_label_size = NumericProperty(100)
    city_main_button_text = StringProperty('縣市')
    city_expanded = False
    city_chosen = BooleanProperty(False)
    city_button_size = NumericProperty(0)
    city_button_opacity = NumericProperty(0)
    city_label_size = NumericProperty(100)
    city_selection = 0
    region_main_button_text = StringProperty('鄉鎮市區')
    region_expanded = False
    region_chosen = False
    regiongroup_button_sizea = NumericProperty(0)
    regiongroup_button_sizeb = NumericProperty(0)
    regiongroup_button_sizec = NumericProperty(0)
    regiongroup_button_sized = NumericProperty(0)
    regiongroup_button_sizee = NumericProperty(0)
    regiongroup_button_sizef = NumericProperty(0)
    regiongroup_button_sizeg = NumericProperty(0)
    regiongroup_button_sizeh = NumericProperty(0)
    regiongroup_button_sizei = NumericProperty(0)
    regiongroup_button_sizej = NumericProperty(0)
    regiongroup_button_sizek = NumericProperty(0)
    regiongroup_button_sizel = NumericProperty(0)
    regiongroup_button_sizem = NumericProperty(0)
    regiongroup_button_sizen = NumericProperty(0)
    regiongroup_button_sizeo = NumericProperty(0)
    regiongroup_button_sizep = NumericProperty(0)
    regiongroup_button_sizeq = NumericProperty(0)
    regiongroup_button_sizer = NumericProperty(0)
    regiongroup_button_sizes = NumericProperty(0)
    regiongroup_button_sizet = NumericProperty(0)
    regiongroup_button_sizeu = NumericProperty(0)
    regiongroup_button_sizev = NumericProperty(0)
    regiongroup_button_opacitya = NumericProperty(0)
    regiongroup_button_opacityb = NumericProperty(0)
    regiongroup_button_opacityc = NumericProperty(0)
    regiongroup_button_opacityd = NumericProperty(0)
    regiongroup_button_opacitye = NumericProperty(0)
    regiongroup_button_opacityf = NumericProperty(0)
    regiongroup_button_opacityg = NumericProperty(0)
    regiongroup_button_opacityh = NumericProperty(0)
    regiongroup_button_opacityi = NumericProperty(0)
    regiongroup_button_opacityj = NumericProperty(0)
    regiongroup_button_opacityk = NumericProperty(0)
    regiongroup_button_opacityl = NumericProperty(0)
    regiongroup_button_opacitym = NumericProperty(0)
    regiongroup_button_opacityn = NumericProperty(0)
    regiongroup_button_opacityo = NumericProperty(0)
    regiongroup_button_opacityp = NumericProperty(0)
    regiongroup_button_opacityq = NumericProperty(0)
    regiongroup_button_opacityr = NumericProperty(0)
    regiongroup_button_opacitys = NumericProperty(0)
    regiongroup_button_opacityt = NumericProperty(0)
    regiongroup_button_opacityu = NumericProperty(0)
    regiongroup_button_opacityv = NumericProperty(0)    
    region_number_list = (12, 13, 13, 18, 26, 13, 20, 18, 33, 16, 13, 6, 7, 3, 2, 12, 38, 29, 29, 37, 4, 6)
    region_label_size = NumericProperty(100)
    color_main_button_text = StringProperty('顏色')
    color_expanded = False
    color_chosen = False
    color_button_size = NumericProperty(0)
    color_button_opacity = NumericProperty(0)
    color_label_size = NumericProperty(100)
    grid_height = NumericProperty(480)
        
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
            if text != '服裝性別':
                global gender_s, gender_r
                gender_s, gender_r= True, result
                self.send_enabled = all((gender_s, city_s, region_s, color_s))

    def region_toggle_expand(self, text):
        self.region_expanded = not self.region_expanded
        si = 100 if self.region_expanded else 0
        op = 1 if self.region_expanded else 0
        city = self.city_selection
        if city & 16:
            if city & 4:
                if city & 1:
                    self.regiongroup_button_sizev = si
                    self.regiongroup_button_opacityv = op
                else:
                    self.regiongroup_button_sizeu = si
                    self.regiongroup_button_opacityu = op
            elif city & 2:
                if city & 1:
                    self.regiongroup_button_sizet = si
                    self.regiongroup_button_opacityt = op
                else:
                    self.regiongroup_button_sizes = si
                    self.regiongroup_button_opacitys = op
            else:
                if city & 1:
                    self.regiongroup_button_sizer = si
                    self.regiongroup_button_opacityr = op
                else:
                    self.regiongroup_button_sizeq = si
                    self.regiongroup_button_opacityq = op
        else:
            if city & 8:
                if city & 4:
                    if city & 2:
                        if city & 1:
                            self.regiongroup_button_sizep = si
                            self.regiongroup_button_opacityp = op
                        else:
                            self.regiongroup_button_sizeo = si
                            self.regiongroup_button_opacityo = op
                    else:
                        if city & 1:
                            self.regiongroup_button_sizen = si
                            self.regiongroup_button_opacityn = op
                        else:
                            self.regiongroup_button_sizem = si
                            self.regiongroup_button_opacitym = op
                else:
                    if city & 2:
                        if city & 1:
                            self.regiongroup_button_sizel = si
                            self.regiongroup_button_opacityl = op
                        else:
                            self.regiongroup_button_sizek = si
                            self.regiongroup_button_opacityk = op
                    else:
                        if city & 1:
                            self.regiongroup_button_sizej = si
                            self.regiongroup_button_opacityj = op
                        else:
                            self.regiongroup_button_sizei = si
                            self.regiongroup_button_opacityi = op
            elif city & 4:
                if city & 2:
                    if city & 1:
                        self.regiongroup_button_sizeh = si
                        self.regiongroup_button_opacityh = op
                    else:
                        self.regiongroup_button_sizeg = si
                        self.regiongroup_button_opacityg = op
                else:
                    if city & 1:
                        self.regiongroup_button_sizef = si
                        self.regiongroup_button_opacityf = op
                    else:
                        self.regiongroup_button_sizee = si
                        self.regiongroup_button_opacitye = op
            elif city & 2:
                if city & 1:
                    self.regiongroup_button_sized = si
                    self.regiongroup_button_opacityd = op
                else:
                    self.regiongroup_button_sizec = si
                    self.regiongroup_button_opacityc = op
            elif city & 1:
                self.regiongroup_button_sizeb = si
                self.regiongroup_button_opacityb = op
            else:
                self.regiongroup_button_sizea = si
                self.regiongroup_button_opacitya = op
        if self.region_expanded:
            self.region_label_size += self.region_number_list[self.city_selection]*100
            self.grid_height += self.region_number_list[self.city_selection]*100
        else:
            self.region_label_size -= self.region_number_list[self.city_selection]*100
            self.grid_height -= self.region_number_list[self.city_selection]*100
            self.region_main_button_text = text
            if text != '鄉鎮市區':
                global region_s, region_r
                region_s, region_r = True, text
                global gender_s, city_s, color_s
                self.send_enabled = all((gender_s, city_s, region_s, color_s))

    def city_toggle_expand(self,text,result=''):
        city_list=('宜蘭縣', '桃園市', '新竹縣', '苗栗縣', '彰化縣', '南投縣', '雲林縣', '嘉義縣', '屏東縣', '臺東縣', '花蓮縣', '澎湖縣', '基隆市', '新竹市', '嘉義市', '臺北市', '高雄市', '新北市', '臺中市', '臺南市', '連江縣', '金門縣')
        self.city_expanded = not self.city_expanded
        if self.city_expanded:
            self.city_button_size = 100
            self.city_button_opacity = 1
            self.city_label_size = 2300
            self.grid_height += 2200
        else:
            self.city_button_size = 0
            self.city_button_opacity = 0
            self.city_main_button_text = text
            if self.region_expanded:
                self.region_toggle_expand('鄉鎮市區')
            else:
                self.region_main_button_text = '鄉鎮市區'
                global region_s, region_r
                region_s, region_r = False, ''
                global gender_s, city_s, color_s
                self.send_enabled = all((gender_s, city_s, region_s, color_s))
            self.city_label_size = 100
            self.grid_height -= 2200
            if text != '縣市':
                self.city_selection = city_list.index(text)
                self.city_chosen = True
                global city_r
                city_s, city_r = True, result
                self.send_enabled = all((gender_s, city_s, region_s, color_s))
    
    def color_toggle_expand(self,text,result=''):
        self.color_expanded = not self.color_expanded
        if self.color_expanded:
            self.color_button_size = 100
            self.color_button_opacity = 1
            self.color_label_size = 1800
            self.grid_height += 1700
        else:
            self.color_button_size = 0
            self.color_button_opacity = 0
            self.color_main_button_text = text
            self.color_label_size = 100
            self.grid_height -= 1700
            if text != '顏色':
                global color_s, color_r
                color_s, color_r = True, result
                global gender_s, city_s, region_s
                self.send_enabled = all((gender_s, city_s, region_s, color_s))
    
    def reset(self):
        if self.region_expanded:
            self.region_toggle_expand('鄉鎮市區')
        else:
            self.region_main_button_text = '鄉鎮市區'
        global region_s, region_r
        region_s, region_r = False, '鄉鎮市區'
        
        if self.color_expanded:
            self.color_toggle_expand('顏色')
        self.color_main_button_text = '顏色'
        global color_s, color_r
        color_s, color_r = False, ''

        if self.gender_expanded:
            self.gender_toggle_expand('服裝性別')
        self.gender_main_button_text = '服裝性別'
        global gender_s, gender_r
        gender_s, gender_r = False, ''

        if self.city_expanded:
            self.city_toggle_expand('縣市')
        self.city_main_button_text = '縣市'
        self.city_chosen = False
        global city_s, city_r
        city_s, city_r = False, ''
        self.send_enabled = all((gender_s, city_s, region_s, color_s))

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
                
class SelectionScreenBoxLayout(BoxLayout):
    pass

class GenderDropDown(StackLayout):
    pass
            
class CityDropDown(StackLayout):
    pass

class RegionDropDown(StackLayout):
    pass

class ColorDropDown(StackLayout):
    pass

class SubGridLayout(GridLayout):
    pass

class ResultScreen(Screen):
    resultimagea = StringProperty('images/na.png')
    resultlabela = StringProperty('無')
    resultimageb = StringProperty('images/na.png')
    resultlabelb = StringProperty('無')
    resultimagec = StringProperty('images/na.png')
    resultlabelc = StringProperty('無')
    resultimaged = StringProperty('images/na.png')
    resultlabeld = StringProperty('無')
    resultimagee = StringProperty('images/na.png')
    resultlabele = StringProperty('無')
    result_text = StringProperty('今天日間平均溫度:')
    result_opacitya = NumericProperty(0)
    result_opacityb = NumericProperty(0)
    result_opacityc = NumericProperty(0)
    result_opacityd = NumericProperty(0)
    result_opacitye = NumericProperty(0)
    

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
    

class ResultScreenBoxLayout(BoxLayout):
    pass

class ResultScreenTitleBoxLayout(BoxLayout):
    pass

class ResultScreenStackLayout(StackLayout):
    pass

class ResultBoxLayoutA(BoxLayout):
    pass

class ResultBoxLayoutB(BoxLayout):
    pass

class ResultBoxLayoutC(BoxLayout):
    pass

class SelectionTitleBoxLayout(BoxLayout):
    pass

class ResultBoxLayoutD(BoxLayout):
    pass

class ResultBoxLayoutE(BoxLayout):
    pass

class MainApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SelectionScreen(name='selection'))
        sm.add_widget(ResultScreen(name='result'))
        sm.current = 'selection'
        return sm

if __name__ == '__main__':
    MainApp().run()