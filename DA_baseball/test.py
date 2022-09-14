from requests_html import HTMLSession, AsyncHTMLSession
from bs4 import BeautifulSoup
session = HTMLSession()
asession = AsyncHTMLSession()

url = 'https://www.cpbl.com.tw/box/index?gameSno=3&year=2022&kindCode=A&fbclid=IwAR1Fl_wMiU6XMreLq9pF7Mxdpn2hGbNkZ65arWBsY3BUaN8Zf7fksJMAaaI'
url2 ='https://www.cpbl.com.tw/box/index?gameSno=3&year=2022&kindCode=A'

r = session.get(url2, verify=False)

r.html.render()
res = r.html.raw_html
print(res[:10])
with open("./DA_baseball/cpbl_v2.txt", "wb") as text_file:
    text_file.write(res)
soup = BeautifulSoup(res, "lxml")
result = soup.findAll('div', {'class': 'GameNote'})
print(result)