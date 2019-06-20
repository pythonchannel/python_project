# coding=gbk

from urllib import parse

from bs4 import BeautifulSoup

str = '%23%E8%87%AA%E5%AA%92%E4%BD%93%E6%95%99%E7%A8%8B%23'
str = parse.unquote(str)

cia = '中国你好'
str = parse.quote(cia)

ssss = '<e type="hashtag" hid="454225848548" title="%23%E8%B5%84%E6%96%99%E5%88%86%E4%BA%AB%23" /> \n和香港第一自媒体Spenser合影，他的一场写作课收费300万，国内Top前10的个人IP.\n\n这里我分享一下他的文章，大家可以看看，学习学习！\n\n链接: <e type="web" href="https%3A%2F%2Fpan.baidu.com%2Fs%2F1I9fVg8DjtONv34AC6dy62w" title="https%3A%2F%2Fpan.baidu.com%2Fs%2F1I9fVg8DjtONv34AC6dy62w" /> 提取码: q8mz 复制这段内容后打开百度网盘手机App，操作更方便哦'

sss = '我发表了一篇文章：<e type="web" href="https%3A%2F%2Farticles.zsxq.com%2Fid_1ra8owb9shl9.html" title="%E6%8E%A8%E5%B9%BF%E5%85%AC%E4%BC%97%E5%8F%B7%E7%9A%84%E6%8A%80%E5%B7%A7" />'

str = '<e type="hashtag" hid="552812421584" title="%23%E6%AF%8F%E6%97%A5%E6%84%9F%E6%82%9F%23" />'

str2 = '<e type="mention" uid="1181242422" title="%40%E5%88%98%E4%B8%8D%E9%B8%A3" />'

str3 = '<e type="web" href="https%3A%2F%2Farticles.zsxq.com%2Fid_1ra8owb9shl9.html" title="%E6%8E%A8%E5%B9%BF%E5%85%AC%E4%BC%97%E5%8F%B7%E7%9A%84%E6%8A%80%E5%B7%A7" />'

s_test = '<e type="hashtag" hid="225114544511" title="%23%E5%AD%A6%E4%B9%A0%E8%B5%84%E6%96%99%23" /> \n\n图片呀\n\n<e type="web" href="https%3A%2F%2Fmp.weixin.qq.com%2Fs%2FODFzKOvawG2P-FHkv14E2A" title="%E9%A1%B9%E7%9B%AE%E5%AE%9E%E6%88%98+%7C+%E6%89%8B%E6%8A%8A%E6%89%8B%E5%B8%A6%E4%BD%A0%E8%8E%B7%E5%8F%96%E6%9F%90%E7%9F%A5%E8%AF%86%E4%BB%98%E8%B4%B9%E5%B9%B3%E5%8F%B0%E5%86%85%E5%AE%B9%E5%88%B6%E4%BD%9C%E7%94%B5%E5%AD%90%E4%B9%A6%EF%BC%88%E4%BA%8C%EF%BC%89" />'

soup = BeautifulSoup(s_test, 'html.parser')

print(parse.unquote(soup.find_all('e')[1]['title']))
print(parse.unquote(soup.find_all('e')[1]['href']))


list = soup.find_all('e')

for l in list:
    if l['type'] == 'web':
        str = '<a href="{}">{}</a>'.format(parse.unquote(l['href']), parse.unquote(l['title']))
        print(str)

# print()
# print(parse.unquote(soup.find_all('e')[1]['title']))
# print(parse.unquote(soup.find_all('e')[1]['href']))


# print(parse.unquote(soup.e2['title']))
# if soup.e.get['href']:
#     print(parse.unquote(soup.e['href']))

# print(soup.e2['type'])

# def deal_tag_e(content):
#     """处理一下e标签内容"""
#     word_mention = '<e type="mention"'
#     word_hashtag = '<e type="hashtag"'
#     word_web = '<e type="web"'
#     if word_mention in content:
#         soup = BeautifulSoup(str3)
#         pass
#     elif word_hashtag in content:
#         pass
#     elif word_web in content:
#         pass


# print(soup)
