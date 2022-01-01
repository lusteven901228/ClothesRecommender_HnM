# 需要的檔案:
# allclothes.csv 每件衣服名稱對應的照片及標籤
# men.csv 男生標籤對應部位及溫度
# women.csv 女生標籤對應部位及溫度

# 輸出的資料：
# 一個list，每項都是一個衣服品項
# .pic 照片 str
# .url 連結 str
# .gender ladies/ men str
# .label label2 + label3 str 
# .color 顏色 str
# .name 品項名稱 str
# .ctype 上身下身分類 int
# .temp 對應溫度 list

import csv

# 開啟檔案
def open_csv(name):
    with open('%s.csv' % name, newline='', encoding="utf-8") as csvfile:
        file = []
        rows = csv.reader(csvfile)
        for row in rows:
            file.append(row)
    return file

allclothesfl = open_csv("allclothes") 
men = open_csv("men")
women = open_csv("women")

# 格式整理
womenlst = []
menlst = []
del men[0], women[0], allclothesfl[0]

for woman in women:
    woman[2], woman[3] = woman[3], woman[2]
    woman[0] = woman[0] + woman[1]
    if woman[4] == "" and (woman[3].isdigit() is True):
        womenlst.append(woman)
    
for i in range(len(allclothesfl)):
    allclothesfl[i][-1].lstrip()
    
for man in men:
    man[0] = man[0] + man[1]
    if man[2] != "x" and (man[3].isdigit() is True):
        menlst.append(man)

#可以的label23
OK_label_m = []
OK_label_w = []
for x in menlst:
    OK_label_m.append(x[0])
for x in womenlst:
    OK_label_w.append(x[0])
    
# class
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

for clothes in finallist:
    if clothes.gender == "ladies":
        clothes.add_ctype_and_temp(womenlst)
    elif clothes.gender == "men":
        clothes.add_ctype_and_temp(menlst)

'''
以上讀檔,以下濾出符合條件衣物並整理成五張表
'''
#輸出五張符合前端條件的列表
#toplist
#bottomlist
#outerlist
#shoeslist
#acclist

#前端給定的條件
# give_temp = 20
# give_color = 'beige'
# give_gender = 'men'

#過濾   
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


'''測試印出
for x in black_bottomlist:
    print(x.name, x.temp, x.color)
'''

import random

bool_dresses = False
bool_shirts = False
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

def ran_bottom(alist, showobjectlst):
    if (not alist) or bool_dresses:
        showobjectlst.append(0)
        return 0
    i = random.randint(0,len(alist)-1)
    showobject = alist[i]
    showobjectlst.append(showobject)
    # 如果上衣是dress, 不要輸出bottom
    return showobject

def ran_outer(alist, showobjectlst):

    while alist:
        i = random.randint(0,len(alist)-1)
        showobject = alist.pop(i)

        if not "knitwear" in showobject.label and not (bool_shirts and "shirts" in showobject.label):
            showobjectlst.append(showobject)
            return showobject
    showobjectlst.append(0)
    return 0
        
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

# 開始輸出，如果選擇要百搭款上衣，whitetopallmatch是True，則用這個清單取隨機
# 如果沒有要百搭，就一般清單取隨機，褲子以此類推
# if whitetop_allmatch = True:
#     ran(white_toplist)
# else:
    ran(toplist, showobjectlst)

# if blackbottom_allmatch = True:
#     ran_bottom(black_bottomlist)
# elif bluebottom_allmatch = True:
#     ran_bottom(blue_bottomlist)
# else:
    ran_bottom(bottomlist, showobjectlst)


    ran_outer(outerlist, showobjectlst)
    ran(shoeslist, showobjectlst)
    ran(acclist, showobjectlst)
    if not showobjectlst[1]:
        showobjectlst[1] = ran(sieve(finallist, give_temp, 'black', give_gender)[1], showobjectlst[:])
    if not showobjectlst[0]:
        showobjectlst[0] = ran(sieve(finallist, give_temp, 'white', give_gender)[1], showobjectlst[:])
    return showobjectlst

if __name__ == "__main__":
    print(*(i.url if i else 0 for i in get_rand_combinations('ladies', 'brown', 23.5)), sep = '\n')
