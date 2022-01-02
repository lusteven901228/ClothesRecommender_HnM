from selenium import webdriver  # sadly, requests doesn't work
from selenium.webdriver.common.by import By
from threading import Thread
from queue import Queue
import re
import time
import pandas as pd  # for better performance and the csv module sucks
'''
1.)selenium required
2.)chromedriver.exe must be at PATH
3.)urls whould be placed in 'HnMurls.txt'
    with each url ending with '\n'
4.)will output a 'HnM.csv' file containg the data
'''
# H&M 'colorWithNames' queries; color_name: colorWithNames
HnM_colors = {'brown': '咖啡色_a52a2a', 'turquoise': '土耳其藍_40e0d0', 'multiple': '多色_000000', 'orange': '橘色_ffa500', 'gray': '灰色_808080', 'white': '白色_ffffff', 'beige': '米色_f5f5dc', 'pink': '粉紅色_ffc0cb', 'red': '紅色_ff0000', 'purple': '紫色_800080', 'green': '綠色_008000', 'blue': '藍色_0000ff', 'gold': '金色_ffd700', 'silver': '銀色_c0c0c0', 'yellow': '黃色_ffff00', 'black': '黑色_000000', 'copper': '古銅色_cd7f32', 'clear': '透明_ffffff'}
HnM_default_query = '?sort=stock&image-size=small&image=stillLife&offset=0&page-size=5000&colorWithNames='
q = Queue()


def HnM(thrs):
    # with open('crawler_test.txt','r') as f:
    with open('HnMurls.txt','r') as f:
        while line:=f.readline():
            q.put(line)
    with open('HnM.csv','w',encoding='utf-8') as f:
        f.write('filename pic_url label1 label2 label3 color name\n')
    t = []  # list of threads
    for _ in range(thrs):
        t.append(Thread(target=HnM_Crawler_thread))  # Calling target each thread
        t[-1].start()
    for i in t:
        i.join() 

# initialize threading drievrs
def HnM_Crawler_thread():
    driver = webdriver.Chrome()
    while not q.empty():
        HnM_Crawler(driver, q.get())
    driver.quit()

def HnM_Crawler(driver, url):
    info = url[url.find('zh_asia3')+9:-6].split('/')  # the urls contain commas so space
    if 'shop-by-product' in info:
        info.remove('shop-by-product')
    if 'basics' in info:
        info.remove('basics')
    info = info[:3]
    for i in range(3-len(info)):
        info.append('')
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

def main():
    thrs = int(input('Chrome thread counts:') or 1) # input thread counts, df=1, less than 10 recommended
    time0 = time.time()
    HnM(thrs)
    time1 = time.time()
    print(time1 - time0)
    df = pd.read_csv('HnM.csv', encoding='utf-8', delimiter='\t', on_bad_lines='skip')
    df.to_csv('allclothes.csv', encoding='utf-8',index=False)
    
if __name__ == '__main__':
    main()
