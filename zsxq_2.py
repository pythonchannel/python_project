import urllib

import requests

import requests
import json

from PyPDF2 import PdfFileWriter, PdfFileReader
from pdfkit import pdfkit
import os


class zsxq_work(object):

    def __init__(self):
        self.zsxq_group_id = []
        self.zsxq_group_name = []
        self.end_time = 0  # 翻页的时间戳
        self.position = 0
        self.my_cookie = 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2216958dd4f79434-0000def4e8ab2e-50422618-2073600-16958dd4f7bfeb%22%2C%22%24device_id%22%3A%2216958dd4f79434-0000def4e8ab2e-50422618-2073600-16958dd4f7bfeb%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%A4%BE%E4%BA%A4%E7%BD%91%E7%AB%99%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fmp.weixin.qq.com%2Fs%3F__biz%3DMzU0NjcwOTYzOQ%3D%3D%26mid%3D2247484043%26idx%3D1%26sn%3D863a41093506585fbc78df023f1e2eb4%26chksm%3Dfb58cb63cc2f427564eb1674c0cb9af153f8abab7cca36dce92226a04b0d417608f3334b879e%26token%3D5064%22%2C%22%24latest_referrer_host%22%3A%22mp.weixin.qq.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%7D%7D; zsxq_access_token=B654A18C-7146-E178-3188-F2E5BFCB6611'

    def get_zsxq_group(self):
        """
         获取知识星球的星球id与名称
        """
        try:
            url_groups = 'https://api.zsxq.com/v1.10/groups'
            headers_group = {
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

            response = requests.get(url=url_groups, headers=headers_group)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                datas = json.loads(response.text, encoding="utf-8").get('resp_data').get('groups')  # 把unicode 编码成 utf-8
                for data in datas:
                    self.zsxq_group_id.append(data.get('group_id'))
                    self.zsxq_group_name.append(data.get('name'))
        except Exception as e:
            print(e.args)

    def get_zsxq_essence_content(self, group_id, group_name):
        """
        因为内容太多，我只想看精华帖子
        :return:
        """

        while True:
            url_content = 'https://api.zsxq.com/v1.10/groups/{}/topics?scope=digests&count=20&end_time={}'.format(
                group_id,
                self.end_time)
            print(url_content)
            content_group = {
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

            response = requests.get(url=url_content, headers=content_group)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                topics = json.loads(response.text, encoding="utf-8").get("resp_data").get(
                    "topics")  # 把unicode 编码成 utf-8
                print(topics)
                if not topics:  # 如果没有主题就退出
                    print('空的')
                    if len(self.zsxq_group_name) > self.position:
                        self.position += 1
                        self.end_time = 0
                        self.get_zsxq_essence_content(xq.zsxq_group_id[xq.position],
                                                      xq.zsxq_group_name[xq.position])
                    break

                end_time = topics[-1].get('create_time')
                self.get_end_time(end_time)

                for topic in topics:
                    try:
                        if topic.get('type') == 'talk' and topic.get('talk'):  # 会话模式的
                            text = topic.get('talk').get('text').replace('\n', '')  # 获取正文内容
                            title = text[0:10] if len(text) > 10 else text
                            author = topic.get('talk').get('owner').get('name')  # 获取作者名称
                            create_time = topic.get('create_time')[:10]  # 获取最后更新时间
                            # images = topic.get('talk').get('images')  # 获取图片列表
                            self.save_zsxq_txt(group_name, title, author.strip(), create_time, text)
                            # if images is not None:
                            #     for image in images:
                            #         imgUrl = image.get('large').get('url')
                            #         print(imgUrl)
                            # else:
                            #     print('没有图片')
                            # print(author, text, modify_time)
                        elif topic.get('type') == 'q&a' and topic.get('question'):
                            author_question = topic.get('question').get('owner').get('name')  # 获取提问者的名称
                            author_answer = topic.get('answer').get('owner').get('name')  # 获取回答者的名称
                            text_question = topic.get('question').get('text').replace('\n', '')  # 获取提问正文
                            text_answer = topic.get('answer').get('text').replace('\n', '')  # 获取回答正文内容
                            title = text_question[0:10] if len(text_question) > 10 else text_question  # 标题
                            text = '{}的提问:{}\n\n{}的回答:{}'.format(author_question, text_question, author_answer,
                                                                 text_answer)  # 获取正文内容
                            author = author_question + '&' + author_answer
                            create_time = topic.get('create_time')[:10]  # 获取最后更新时间
                            # images = topic.get('question').get('images')  # 获取图片列表
                            self.save_zsxq_txt(group_name, title, author.strip(), create_time, text)
                            # if images is not None:
                            #     for image in images:
                            #         imgUrl = image.get('large').get('url')
                            #         print(imgUrl)
                            # else:
                            #     print('没有图片')
                            # print(author, text, modify_time)
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

    def save_pdf(html, filename):
        """
        把所有html文件保存到pdf文件
        :param html:  html内容
        :param file_name: pdf文件名
        :return:
        """
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }

        pdfkit.from_string(html, filename, options=options)

    def parse_html_to_pdf(self):
        """
        解析URL，获取html，保存成pdf文件
        :return: None
        """
        try:
            for chapter in chapter_info:
                ctitle = chapter['title']
                url = chapter['url']
                # 文件夹不存在则创建（多级目录）
                dir_name = os.path.join(os.path.dirname(__file__), 'gen', ctitle)
                if not os.path.exists(dir_name):
                    os.makedirs(dir_name)

                html = get_content(url)

                padf_path = os.path.join(dir_name, ctitle + '.pdf')
                save_pdf(html, os.path.join(dir_name, ctitle + '.pdf'))

                children = chapter['child_chapters']
                if children:
                    for child in children:
                        html = get_content(child['url'])
                        pdf_path = os.path.join(dir_name, child['title'] + '.pdf')
                        save_pdf(html, pdf_path)

        except Exception as e:
            print(e)

    def merge_pdf(infnList, outfn):
        """
        合并pdf
        :param infnList: 要合并的PDF文件路径列表
        :param outfn: 保存的PDF文件名
        :return: None
        """
        pagenum = 0
        pdf_output = PdfFileWriter()

        for pdf in infnList:
            # 先合并一级目录的内容
            first_level_title = pdf['title']
            dir_name = os.path.join(os.path.dirname(
                __file__), 'gen', first_level_title)
            padf_path = os.path.join(dir_name, first_level_title + '.pdf')

            pdf_input = PdfFileReader(open(padf_path, 'rb'))
            # 获取 pdf 共用多少页
            page_count = pdf_input.getNumPages()
            for i in range(page_count):
                pdf_output.addPage(pdf_input.getPage(i))

            # 添加书签
            parent_bookmark = pdf_output.addBookmark(
                first_level_title, pagenum=pagenum)

            # 页数增加
            pagenum += page_count

            # 存在子章节
            if pdf['child_chapters']:
                for child in pdf['child_chapters']:
                    second_level_title = child['title']
                    padf_path = os.path.join(dir_name, second_level_title + '.pdf')

                    pdf_input = PdfFileReader(open(padf_path, 'rb'))
                    # 获取 pdf 共用多少页
                    page_count = pdf_input.getNumPages()
                    for i in range(page_count):
                        pdf_output.addPage(pdf_input.getPage(i))

                    # 添加书签
                    pdf_output.addBookmark(
                        second_level_title, pagenum=pagenum, parent=parent_bookmark)
                    # 增加页数
                    pagenum += page_count

        # 合并
        pdf_output.write(open(outfn, 'wb'))
        # 删除所有章节文件
        shutil.rmtree(os.path.join(os.path.dirname(__file__), 'gen'))

    def save_zsxq_txt(self, group_name, title, author, create_time, content):
        try:
            txt_path = u'd:/zsxq'
            txt_name = u'{}.txt'.format(group_name)
            # 写入txt文本
            with open(txt_path + '/' + txt_name, 'a', encoding='utf-8') as f:
                msg = '标题: {}\n作者:{}\n创建时间:{}\n\n{}\n\n\n\n\n'.format(title, author, create_time, content)
                f.write(msg)
        except Exception as e:
            print(e.message)


if __name__ == '__main__':
    xq = zsxq_work()
    xq.get_zsxq_group()
    print(xq.zsxq_group_name)
    xq.get_zsxq_essence_content(xq.zsxq_group_id[xq.position], xq.zsxq_group_name[xq.position])
    # for i in range(len(xq.zsxq_group_id)):
    #     xq.end_time = 0  # 每换一个星球群组，需要把时间戳重置下
    #     xq.get_zsxq_essence_content(xq.zsxq_group_id[xq.position], xq.zsxq_group_name[xq.position])
