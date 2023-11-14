import requests
import re
from bs4 import BeautifulSoup
import time
import os


# 获取网站
def getHTMLText(url):
    r = requests.get(url)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    html = r.text
    return html


# 得到该页的图片文件夹，一共12个
def getFirstFile(html, img_1_name, img_1_html):
    soup_1 = BeautifulSoup(html, "html.parser")
    plt_1 = soup_1.find_all('div', class_="blog-title")

    # 获取图片的名称和文件地址
    Re_1_html = re.findall('<a href="(.*?)">.*?</a>', str(plt_1))
    Re_1_name = re.findall('<a href=".*?">(.*?)</a>', str(plt_1))
    for name in Re_1_name:
        img_1_name.append(name)
    for i in range(len(Re_1_html)):
        img_1_html.append(Re_1_html[i])

# 创建目录
def creatFilesName(fileName,img_1_name):
    files_name = '性感小姐姐'
    if not os.path.exists(files_name):
        os.mkdir(files_name)
    for name in img_1_name:
        file_name = files_name + '/' + name
        if not os.path.exists(file_name):
            os.mkdir(file_name)
        fileName.append(file_name)    

# 获取图片的地址
def getimgsHTML(html, imgs):
    soup_2 = BeautifulSoup(html, "html.parser")
    plt_2 = soup_2.find('div', class_="blog-details-text")
    Re_img = re.findall('src="(.*?)"', str(plt_2))
    for each in Re_img:
        imgs.append(each)
    return imgs


# 爬取图片，休眠为5秒
def getImgPhoto(fileName, imgs, j):
    for i in range(len(imgs)):
        time.sleep(2)
        img = imgs[i]
        print(img)
        r = requests.get(img)
        with open(fileName[j] + '/' + str(i) + '.jpg', 'wb') as f:
            f.write(r.content)

# 实现函数
def main():
    for n in range(3, 4):
        img_1_name = []
        img_1_html = []
        fileName = []
        url_1 = 'https://mm.tvv.tw/page/' + str(n) + '/'
        html = getHTMLText(url_1)
        getFirstFile(html, img_1_name, img_1_html)
        creatFilesName(fileName, img_1_name)
        # 将每一个图片文件夹j的每一张图片保存
        for j in range(len(img_1_name)):
            print(img_1_name[j])
            imgs = []
            html = getHTMLText(img_1_html[j])  #得到文件夹地址
            getimgsHTML(html, imgs)  #得到图片地址序列
            getImgPhoto(fileName, imgs, j)

main()

