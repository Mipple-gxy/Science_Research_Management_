# -*- coding: utf-8 -*- 
# @Author: Cheung Y.H.
# @Date  : 2021/11/11
# version: Python 3.9.2

import requests
from bs4 import BeautifulSoup
import os

path = ".\\downloadArticles\\"
if os.path.exists(path) == False:
    os.mkdir(path)  #创建保存下载文章的文件夹，与py文件在同一个文件夹下
f = open("doi.txt", "r", encoding="utf-8")  #存放DOI码的.txt文件中，每行存放一个文献的DOI码，完毕须换行（最后一个也须换行）
head = {\
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'\
            }  #防止HTTP403错误
for line in f.readlines():
    line = line[:-1] #去换行符
    url = "https://www.sci-hub.ren/" + line + "#" #sci hub检索地址，若找不到需要自行寻找检索地址源
    try:
        download_url = ""  
        r = requests.get(url, headers = head)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        soup = BeautifulSoup(r.text, "html.parser")
       
        if soup.iframe == None:  
            download_url = "https:" + soup.embed.attrs["src"] 
        else:
            download_url = soup.iframe.attrs["src"]  
        print(line + " is downloading...\n  --The download url is: " + download_url)
        download_r = requests.get(download_url, headers = head)
        download_r.raise_for_status()
        with open(path + line.replace("/","_") + ".pdf", "wb+") as temp:
            temp.write(download_r.content)
    except:
        with open("error.txt", "a+") as error:
            error.write(line + " occurs error!\n")
            if "https://" in download_url:
                error.write(" --The download url is: " + download_url + "\n\n")
    else:
        download_url = "" 
        print(line + " download successfully.\n")
f.close()
