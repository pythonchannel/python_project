import urllib

import requests
import json

from PyPDF2 import PdfFileWriter, PdfFileReader
import pdfkit
import os


class zsxq_work(object):

    def __init__(self):
        self.zsxq_group_id = []
        self.zsxq_group_name = []
        self.config = pdfkit.configuration(
            wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # 这里需要配置一下wkhtmlpdf.exe路径
        self.end_time = 0  # 翻页的时间戳
        self.html_template = """
                            <!DOCTYPE html>
                            <html lang="en">
                            <head>
                                <meta charset="UTF-8">
                            </head>
                            <body>
                            <h1>{title}</h1>
                            <h6>{author_time}</h6>
                            <p font-size = '35px'>{text}</p>
                             <img src = {images}>                    
                            </body>
                            </html>
                            """
        self.html_contents = []
        self.my_cookie = 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216958dd4f79434-0000def4e8ab2e-50422618-2073600-16958dd4f7bfeb%22%2C%22%24device_id%22%3A%2216958dd4f79434-0000def4e8ab2e-50422618-2073600-16958dd4f7bfeb%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU0NjcwOTYzOQ%3D%3D%26mid%3D2247484043%26idx%3D1%26sn%3D863a41093506585fbc78df023f1e2eb4%26chksm%3Dfb58cb63cc2f427564eb1674c0cb9af153f8abab7cca36dce92226a04b0d417608f3334b879e%26token%3D5064%22%2C%22%24latest_referrer_host%22%3A%22mp.weixin.qq.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; zsxq_access_token=02524B6A-A9F4-D890-3A2C-152C6E4F002C'
        self.zsxq_headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Cookie': self.my_cookie,
            'Host': 'api.zsxq.com',
            'Origin': 'https://wx.zsxq.com',
            'Referer': 'https://wx.zsxq.com/dweb/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
        }

    def get_zsxq_group(self):
        """
         获取知识星球的星球id与名称
        """
        try:
            url_groups = 'https://api.zsxq.com/v1.10/groups'
            response = requests.get(url=url_groups, headers=self.zsxq_headers)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                datas = json.loads(response.text, encoding="utf-8").get('resp_data').get('groups')  # 把unicode 编码成 utf-8
                for data in datas:
                    self.zsxq_group_id.append(data.get('group_id'))
                    self.zsxq_group_name.append(data.get('name'))
        except Exception as e:
            print(e.args)

    def get_zsxq_essence_content_pdf(self, type, group_id, group_name):
        """
        @:type 0 就是普通帖子 1 代表精华帖子

        """
        while True:
            # 精华帖子
            url_content_essence = 'https://api.zsxq.com/v1.10/groups/{}/topics?scope=digests&count=20&end_time={}'.format(
                group_id,
                self.end_time)
            # 普通帖子
            url_content_normal = 'https://api.zsxq.com/v1.10/groups/{}/topics?count=20&end_time={}'.format(
                group_id,
                self.end_time)
            response = requests.get(url=url_content_essence if type > 0 else url_content_normal,
                                    headers=self.zsxq_headers)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                topics = json.loads(response.text, encoding="utf-8").get("resp_data").get(
                    "topics")  # 把unicode 编码成 utf-8
                print(topics)
                if not topics:  # 如果没有主题就退出
                    print('数据加载完毕,开始制作pdf文档')
                    self.creat_pdf_file(group_name)
                    break

            end_time = topics[-1].get('create_time')
            self.get_end_time(end_time)

            for topic in topics:
                try:
                    if topic.get('type') == 'talk' and topic.get('talk'):  # 会话模式的
                        text = topic.get('talk').get('text').replace('\n', '')  # 获取正文内容
                        title = text[0:20] if len(text) > 20 else text
                        author = topic.get('talk').get('owner').get('name')  # 获取作者名称
                        create_time = (topic.get('create_time')[:20]).replace('T', ' ')  # 获取最后更新时间
                        author_time = '{}在{}发表'.format(author, create_time)

                        images = topic.get('talk').get('images')  # 获取图片列表
                        img = []
                        if images is not None:
                            for image in images:
                                img = image.get('large').get('url')
                            # img.append(image.get('large').get('url'))

                        title = title if len(title) > 0 else '无标题'
                        html_content = self.html_template.format(title=title, author_time=author_time, text=text,
                                                                 images=img)
                        self.html_contents.append(html_content)
                    elif topic.get('type') == 'q&a' and topic.get('question'):

                        if topic.get('question').get('owner'):
                            author_question = topic.get('question').get('owner').get('name')  # 获取提问者的名称
                        else:
                            author_question = "匿名提问"  # 获取提问者的名称

                        author_answer = topic.get('answer').get('owner').get('name')  # 获取回答者的名称
                        text_question = topic.get('question').get('text').replace('\n', '')  # 获取提问正文
                        text_answer = topic.get('answer').get('text').replace('\n', '')  # 获取回答正文内容
                        title = text_question[0:20] if len(text_question) > 20 else text_question  # 标题
                        text = '{}的提问:{}\n\n{}的回答:{}'.format(author_question, text_question, author_answer,
                                                             text_answer)  # 获取正文内容
                        author = author_question + '&' + author_answer
                        create_time = (topic.get('create_time')[:20]).replace('T', '')  # 获取最后更新时间
                        # images = topic.get('question').get('images')  # 获取图片列表

                        author_time = '{}在{}发表'.format(author, create_time)
                        img = []
                        if images is not None:
                            for image in images:
                                img = image.get('large').get('url')
                                # img.append(image.get('large').get('url'))
                        title = title if len(title) > 0 else '无标题'
                        html_content = self.html_template.format(title=title, author_time=author_time, text=text,
                                                                 images=img)
                        self.html_contents.append(html_content)

                except Exception as e:
                    print(e.args)

    def get_end_time(self, create_time):
        """
        获取翻页的时间戳
        :param create_time:
        :return:
        """
        first_time = create_time[:10]  # 前一部分时间
        middle_time = create_time[10:-4]  # 中间一部分时间
        last_time = create_time[-4:]  # 最后一部分时间
        change_middle_time = middle_time.replace(middle_time[-4:-1], str(int(middle_time[-4:-1]) - 1).zfill(
            3))  # 1. 网页列表的时间戳，发现规律，时间戳倒数第5位会比前面最后一页的时间戳少1 2. zfill方法可以在左边补0 凑成3位

        self.end_time = first_time + urllib.parse.quote(change_middle_time) + last_time
        print(self.end_time)

    def creat_pdf_file(self, group_title):
        htmls = []  # 这里是存放html文件

        for index, file in enumerate(self.html_contents):
            html = '{}.html'.format(index)
            with open(html, 'w', encoding='utf-8') as f:  # 点击open函数查看用法，这里是写入不要搞错了
                f.write(file)

            htmls.append(html)

        try:
            output_file = 'D:/zsxq2/{}.pdf'.format(group_title)
            if not os.path.exists(output_file):  # 过滤掉重复文件
                pdfkit.from_file(htmls, output_file, configuration=self.config)  # 注意这里需要配置一下wkhtmltopdf
        except Exception as e:
            print(e)


if __name__ == '__main__':
    xq = zsxq_work()
    xq.get_zsxq_group()
    # xq.get_zsxq_essence_content_pdf(0, xq.zsxq_group_id[0], xq.zsxq_group_name[0])
    for i in range(len(xq.zsxq_group_id)):
        xq.end_time = 0  # 每换一个星球群组，需要把时间戳重置下
        xq.html_contents = []  # 清空一下网页内容
        xq.get_zsxq_essence_content_pdf(0, xq.zsxq_group_id[i], xq.zsxq_group_name[i])
