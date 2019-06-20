import json
import os

import pdfkit
import requests
import time


class wx_gzh(object):

    def __init__(self):

        self.urls = [
            'https://mp.weixin.qq.com/s/iH7HFEup3Buue6bJBIDLpA',
            'https://mp.weixin.qq.com/s/2rFbJ-O2BsHbJTTc2Y6DCQ',
            'https://mp.weixin.qq.com/s/398e6QnA120k4SMuWI9YnQ',
            'https://mp.weixin.qq.com/s/iH7HFEup3Buue6bJBIDLpA',
            'https://mp.weixin.qq.com/s/pBub3TiKcNqOzTIy5hXvUw',
            'https://mp.weixin.qq.com/s/vZBh0U9ukPUvHG34WK8FyQ',
            'https://mp.weixin.qq.com/s/RTyTzFzeOIvzdDBtPFFebQ',
            'https://mp.weixin.qq.com/s/ODFzKOvawG2P-FHkv14E2A',
            'https://mp.weixin.qq.com/s/RCMAOdTTdNw058B-qcm7Jw'
        ]
        self.article_msg = [{
            "id": 2,
            "my_id": 20,
            "nick_name": "刘不鸣",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/AlBInLckA7RRiaNibEt0rM307m1hMT2goY77BXIXsNt1zqtC3Vy9pHOVNw3cuNEKvu0Ru1PGZS41QnUL3PIiaPgOFXzhXr1bzba\/132",
            "content": "收藏就行了！",
            "create_time": 1560743504,
            "content_id": "5282525533144350740",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 1,
            "reply": {
                "reply_list": []
            },
            "is_from_me": 0,
            "is_top": 1
        }, {
            "id": 8,
            "my_id": 81,
            "nick_name": "小肥仔",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/Q3auHgzwzM7VBMdia3ianWF8s3pD7zK7XibOPGiaU8poPBrsiaLicAkkGY1YjqNiaawQcG9u6NZwd1dNJejaQFfbYMlGSA90EUzwEvSm4iatItl1NRk\/132",
            "content": "day54 果断收藏啦[憨笑]",
            "create_time": 1560749704,
            "content_id": "5682503339065999441",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 0,
            "reply": {
                "reply_list": []
            },
            "is_from_me": 0,
            "is_top": 0
        }, {
            "id": 7,
            "my_id": 9,
            "nick_name": "神魂祭天",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/ySIckcWvB1kzfoibJpepYzdLZ5EibKMj2On05sadCRjXOKbeNYDI6qngjVAibxgxicqnM7HQhMoFYu8W8xWQJQLWdTZ9V1vgvBXe\/132",
            "content": "这才是真正的干货",
            "create_time": 1560746926,
            "content_id": "2089308019622936585",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 0,
            "reply": {
                "reply_list": []
            },
            "is_from_me": 0,
            "is_top": 0
        }, {
            "id": 6,
            "my_id": 467,
            "nick_name": "The one | LifeHacker",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/ySIckcWvB1kzfoibJpepYzQbjIm71C7RDn5c5JrYDCu3LQzA9OdUpibqOLStOspd1x9rUzFF2LeX77ljgQGcWNicLR3ZEB5WrYH\/132",
            "content": "妥妥的干货！[强][强][强]",
            "create_time": 1560745992,
            "content_id": "2745342786365555155",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 0,
            "reply": {
                "reply_list": []
            },
            "is_from_me": 0,
            "is_top": 0
        }, {
            "id": 5,
            "my_id": 255,
            "nick_name": "小阿信",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/AlBInLckA7TT8KPDh9Pt6VJftsMzChtd2AD2VD5hHtlRhibJibKMCMnYUudaNbbSnvWZ2LP3yLlRF9WcACfbWmP3zmGEAEmby4\/132",
            "content": "Day66，收藏了[机智]",
            "create_time": 1560744504,
            "content_id": "6581265300619002111",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 0,
            "reply": {
                "reply_list": []
            },
            "is_from_me": 0,
            "is_top": 0
        }, {
            "id": 4,
            "my_id": 1409,
            "nick_name": "刘不鸣",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/b9LMD3uzD8rkOrbdP32M1p3I36412LbuW0TxtibVUygr5BPDREStxH8iberRVicBKzp4O6mGIH7kwyib4kmhD001qUnc1XGZFUl6\/132",
            "content": "牛逼牛逼！",
            "create_time": 1560744205,
            "content_id": "88492453899797889",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 1,
            "reply": {
                "reply_list": []
            },
            "is_from_me": 0,
            "is_top": 0
        }, {
            "id": 3,
            "my_id": 260,
            "nick_name": "部落大圣",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/AlBInLckA7Qx2t3cjfspnFdjcA1g2n82eXLU5F3TCqGIwoic0xsORM6BhDjCquKLhebxdymSUlJMfI08tN1ssGmWsfJOP4F9X\/132",
            "content": "Day 80，真干货收藏了",
            "create_time": 1560743673,
            "content_id": "7843265952203407620",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 0,
            "reply": {
                "reply_list": []
            },
            "is_from_me": 0,
            "is_top": 0
        }, {
            "id": 1,
            "my_id": 9,
            "nick_name": "快乐的猴子",
            "logo_url": "http:\/\/wx.qlogo.cn\/mmopen\/ySIckcWvB1kzfoibJpepYzWBRLYZBjSDEg9w8ps30mlqc44KaH9NgyOxrHf2w5NrnkC74V8ibnycvVEbaGdQ0KHnxLhKvTIwXN\/132",
            "content": "真正的干货呀！",
            "create_time": 1560743336,
            "content_id": "2862119236292050953",
            "like_id": 0,
            "like_num": 0,
            "like_status": 0,
            "is_from_friend": 0,
            "reply": {
                "reply_list": [{
                    "content": "都是辛勤整理的",
                    "uin": 2391486077,
                    "create_time": 1560743448,
                    "reply_id": 1,
                    "to_uin": 666389064
                }]
            },
            "is_from_me": 1,
            "is_top": 0
        }]
        self.config = pdfkit.configuration(
            wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # 这里需要配置一下wkhtmlpdf.exe路径
        self.html_contents = []
        self.zsxq_headers = {
        }

    def request_artiacl_content(self):
        """
         获取知识星球的星球id与名称
        """
        try:
            for url in self.urls:
                response = requests.get(url=url, headers=self.zsxq_headers)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
                if response.status_code == 200:  # 注意：这里一定要做200判断，
                    self.html_contents.append(
                        self.create_article_content(url, response.text) + self.create_article_msgboard())
                    self.creat_pdf_file()
                else:
                    continue
        except Exception as e:
            print(e.args)


    def create_article_content(self, url, text):
        """文章内容"""

        str = '<span style="font-size:30px"><a href = "{}">公众号原文地址</a></span><br>'.format(
            url) + text.replace('data-src', 'src') + '<br> <span style="font-size:30px">留言板</span><br>'

        return str

    def create_article_msgboard(self):
        """文章评论"""
        all_datas = json.loads(self.article_msg)

        if all_datas:
            msg_box_str = ''
            for data in all_datas:
                msg_str = ''
                logo_url = data['logo_url']
                nick_name = data['nick_name']
                content = data['content']
                create_time = data['create_time']
                like_num = data['like_num']
                '<img src="{}"> 昵称：{}留言时间：{}，点赞数量:{}<br>{}'.format(logo_url, nick_name, self.time_long2str(create_time),
                                                                   like_num, content)
                reply_list = data['reply']['reply_list']
                if reply_list:
                    msg_str.join('<br>小编回复:</br>{}<br>回复时间：{}'.format(reply_list[0]['content'],
                                                                      self.time_long2str(reply_list[0]['create_time'])))
                msg_str.join('<br><hr/>')
                msg_box_str.join(msg_str)  # 追加评论



        else:
            return '<span style="font-size:30px">无留言</span>'

    def creat_pdf_file(self, group_title):
        htmls = []  # 这里是存放html文件

        for index, file in enumerate(self.html_contents):
            html = '{}.html'.format(index)
            with open(html, 'w', encoding='utf-8') as f:  # 点击open函数查看用法，这里是写入不要搞错了
                f.write(file)

            htmls.append(html)

        try:
            output_file = 'D:/gzh2/{}.pdf'.format(group_title)
            if not os.path.exists(output_file):  # 过滤掉重复文件
                pdfkit.from_file(htmls, output_file, configuration=self.config,
                                 )  # 注意这里需要配置一下wkhtmltopdf
        except Exception as e:
            print(e)
        finally:
            for html_file in htmls:  # 清除生成的html文件
                os.remove(html_file)

    pass

    def time_long2str(self,timeStamp):
        """把long类型的时间转换成字符串形式"""
        timeArray = time.localtime(timeStamp)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return strTime[:10]


if __name__ == '__main__':
    gzh = wx_gzh()
    gzh.request_artiacl_content()
