import json
import os

import pdfkit
import requests
import time

import sys
import warnings

warnings.filterwarnings("ignore")


class wx_gzh(object):

    def __init__(self):

        """
        注意这里面的
        baseurl
        cookie
        referer
        三个数据都有可能发生变化，所以每次取的时候，要用最新的，可以在charles中获取
        """
        self.config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        self.offset = 100
        self.count = 0
        self.index_part = 0
        self.part_offset = 25
        self.gzh_name = 'Spenser'
        self.base_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzA3NjU2MDUzMA==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=NjY2Mzg5MDY0&key=6ff676ea8e4091fdbdcf264f9bccd600e817aa6372497b9d04a4e7c0633341e60d536687592a3a3a1ad1f2a37a0cefe333f1ff55cec5fe9d1378a1548cbeb64ff6ab9c9b11fd6a3d0b97d709610a25ba&pass_ticket=5Zx%2F6KSKXNBH%2BaeYBg4b7bKsVQxXIMf%2BS8GiZKBneQiu9dtMJzUuN33ddCWWtnnf&wxtoken=&appmsg_token=1014_jS%252B2zAyNaYUzghPp_0uOKO87-X1y-KxA4BDeDQ~~&x5=0&f=json'
        self.cookie = 'rewardsn=; wxtokenkey=777; wxuin=666389064; devicetype=Windows10; version=62060833; lang=zh_CN; pass_ticket=5Zx/6KSKXNBH+aeYBg4b7bKsVQxXIMf+S8GiZKBneQiu9dtMJzUuN33ddCWWtnnf; wap_sid2=CMiU4b0CElxVbDNxT0d6Yk10RkowbWFOQWhWQUtMQlhGVTF4aXZPbFpBQXpjakR1ajZic1lBVWlPOHQzdm42MC1XNWY2OFZxQTFzLXVLVDF5S3BYX2hrcXBYVUVNUFlEQUFBfjCQnKnoBTgNQJVO'
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400',
            'X-Requested-With': 'XMLHttpRequest',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Cookie': self.cookie
        }
        self.html_contents = []

    def request_data(self):
        try:
            response = requests.get(self.base_url.format(self.offset), headers=self.headers)
            if 200 == response.status_code:
                self.parse_data(response.text)
        except Exception as e:
            print(sys._getframe().f_code.co_name)
            print(e.args)

    def parse_data(self, response_data):
        all_datas = json.loads(response_data)
        if 0 == all_datas['ret']:
            if 1 == all_datas['can_msg_continue']:
                summy_datas = all_datas['general_msg_list']
                datas = json.loads(summy_datas)['list']
                for data in datas:
                    try:

                        article_url = data['app_msg_ext_info']['content_url']
                        copyright = data['app_msg_ext_info']['copyright_stat']
                        if copyright != 11:  # 这里只生成原创文章
                            continue

                        self.request_artiacl_html(article_url)

                        self.count += 1  # 记录文件
                        print('准备第{}个文件'.format(str(self.count)))
                        if self.count % self.part_offset == 0:  # 每10篇文章为一部分
                            self.index_part += 1
                            print('准备生成第【{}】部分文件...'.format(str(self.index_part)))
                            self.creat_pdf_file()

                    except Exception as e:
                        print(e.args)
                        continue

                time.sleep(1)
                self.offset = all_datas['next_offset']  # 下一页的偏移量
                self.request_data()
            else:
                print('数据抓取完毕！')

        else:
            exit('数据抓取出错:' + all_datas['errmsg'])

    def time_long_to_str(self, time_stamp):
        """把long类型的时间转换成字符串形式"""
        timeArray = time.localtime(time_stamp)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return strTime[:10]

    def request_artiacl_html(self, url):
        """
         根据文章的url地址获取他的网页源代码，来拼接出pdf
        """
        try:
            response = requests.get(url=url, headers=self.headers)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                self.html_contents.append(self.create_article_content(url, response.text))

        except Exception as e:
            print(sys._getframe().f_code.co_name)
            print(e.args)
            raise

    def create_article_content(self, url, text):
        """文章内容"""
        str = '<span style="font-size:30px; padding:10px"><a href = "{}">点击查看公众号原文</a></span>'.format(
            url) + text.replace('data-src', 'src')
        return str

    def creat_pdf_file(self):

        htmls = []
        for index, file in enumerate(self.html_contents):
            html = '{}.html'.format(index)  # 这里是存放临时html文件
            with open(html, 'w', encoding='utf-8') as f:  # 点击open函数查看用法，这里是写入不要搞错了
                f.write(file)

            htmls.append(html)

        try:
            output_file = 'D:/gzh2/{}_的原创文章_第【{}-{}】篇.pdf'.format(self.gzh_name,
                                                                  (self.index_part - 1) * self.part_offset + 1,
                                                                  self.index_part * self.part_offset)
            if not os.path.exists(output_file):  # 过滤掉重复文件
                pdfkit.from_file(htmls, output_file, configuration=self.config,
                                 )  # 注意这里需要配置一下wkhtmltopdf
        except Exception as e:
            print(sys._getframe().f_code.co_name)
            print(e)
        finally:
            self.html_contents = []  # 生成文件后，清空缓存
            for file in htmls:
                os.remove(file)


if __name__ == '__main__':
    gzh = wx_gzh()
    gzh.request_data()
