import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

meta_url = "https://www.koscom.co.kr/portal/bbs/B0000034/list.do?searchCnd=&searchWrd=&gubun=&delcode=0&searchBgnDe=&searchEndDe=&useAt=&replyAt=&menuNo=200327&sdate=&edate=&deptId=&isk=&ise=&viewType=&type=&year="

title_list = []
sub_title_list = []
content_list = []

for page in range(1, 32):
    url = '{}&pageIndex={}'.format(meta_url, page)
    html = requests.get(url, headers={'User-agent': 'Mozilla/5.0'}).text
    soup = bs(html, 'html.parser')
    titles = soup.find_all("strong", {"class" : "cor_red em"})

    for i in titles:
        title = str(i).replace('<strong class="cor_red em">', '').replace('</strong>', '')
        title_list.append(title)

    sub_titles = soup.find_all("span", {"class" : "em"})

    for i in sub_titles:
        sub_title = str(i).replace('<span class="em">', '').replace('</span>', '')
        sub_title_list.append(sub_title)

    contents = soup.find_all("p", class_="con_hid")

    for i in contents[1::2]:
        content = str(i).replace('<p class="con_hid">', '').replace('</p>', '').strip()
        content_list.append(content) 

df = pd.DataFrame((zip(title_list, sub_title_list, content_list)), columns = ['TItle', 'Sub_Title', 'Content'])
df.to_excel('ITwordfromKoscom.xlsx')