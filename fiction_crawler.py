import requests
import re
import time
from bs4 import BeautifulSoup


def get_html(url):  # 获取网页
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36'
    }
    html = ''
    flag = False
    while flag == False:
        try:
            response = requests.get(url, headers=headers)
            response.encoding = 'utf-8'
            if response.status_code != 200:
                raise Exception("error")
            flag = True
            print('get success')
        except:
            print('get fail')
    html = response.text
    return html


def get_content(html):  # 获取目录链接
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('dd')
    list_urls = re.findall('<a href="(.*?)"', str(urls))
    print(list_urls)
    return list_urls


def get_context(html):  # 获取正文内容
    soup = BeautifulSoup(html, 'lxml')
    title = soup.find("div", {'id': 'title'}).get_text()
    print(title)
    context = soup.find("div", {'id': 'content'}).get_text()
    context = context.replace('\xa0', ' ')
    context = context.replace('\r', '\n')
    context = title + '\n\r' + context
    return context

def get_next(html): # 获取下一页
    soup = BeautifulSoup(html, 'lxml')
    tag = soup.find('div', {'id': 'footlink'})
    _next = re.findall('<a href="(.*)">下一页', str(tag.contents[9]))
    url_next = 'http://www.bxwx8.la/b/2/2933/' + _next[0]
    return url_next

if __name__ == "__main__":
    print('craw content...')
    txt_file = open("大道朝天.txt", "w+", encoding='utf-8')
    url = 'http://www.bxwx8.la/b/2/2933/476030.html'
    html = get_html(url)
    context = get_context(html) + '\n\r'
    txt_file.write(context)
    # urls_content = get_content(html)
    nextUrl = get_next(html)
    while nextUrl != 'http://www.bxwx8.la/b/2/2933/index.html':
        nextPage = get_html(nextUrl)
        context = get_context(nextPage) + '\n\r'
        txt_file.write(context)     
        nextUrl = get_next(nextPage)
    txt_file.close()
