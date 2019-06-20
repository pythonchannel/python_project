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
        self.offset = 0
        self.count = 0
        self.gzh_name = '沈小星'
        self.base_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzI0NTY2MjQ5OQ==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=NjY2Mzg5MDY0&key=6ff676ea8e4091fdc75bc0022cb71cd0e3c28e8366cdc913f01155d20369371b91700a01e09fb340ad4ed16ea6c70ee995b3e9fd98f327090780eaff139733f1bc1cb04d25f52089693b82e9947614fd&pass_ticket=5Zx%2F6KSKXNBH%2BaeYBg4b7bKsVQxXIMf%2BS8GiZKBneQiu9dtMJzUuN33ddCWWtnnf&wxtoken=&appmsg_token=1014_jcUhJ3%252B3aQqLzcivNJKdirGVakFRgMwj0CNsqg~~&x5=0&f=json'
        self.cookie = 'rewardsn=; wxtokenkey=777; wxuin=666389064; devicetype=Windows10; version=62060833; lang=zh_CN; pass_ticket=5Zx/6KSKXNBH+aeYBg4b7bKsVQxXIMf+S8GiZKBneQiu9dtMJzUuN33ddCWWtnnf; wap_sid2=CMiU4b0CElxVbDNxT0d6Yk10RkowbWFOQWhWQUtFek1YUUpVQlVPTVdmcEtzNlRfTWdQT0JlM0JMa2hjc0c1TVRPZW5tS2xtTzlkdC1ZaHk0T1Rtb3d0VnNsbmpUZllEQUFBfjChvajoBTgNQJVO'
        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400',
            'X-Requested-With': 'XMLHttpRequest',
            #  'Referer': self.referer,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Cookie': self.cookie
        }
        self.article_msg = []
        self.config = pdfkit.configuration(
            wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')  # 这里需要配置一下wkhtmlpdf.exe路径

    def request_data(self):
        response = requests.get(self.base_url.format(self.offset), headers=self.headers)
        if 200 == response.status_code:
            self.parse_data(response.text)

    def parse_data(self, response_data):
        all_datas = json.loads(response_data)
        if 0 == all_datas['ret']:
            if 1 == all_datas['can_msg_continue']:
                summy_datas = all_datas['general_msg_list']
                #  print(summy_datas)
                datas = json.loads(summy_datas)['list']
                for data in datas:
                    try:
                        title = data['app_msg_ext_info']['title']
                        article_time = self.time_long_to_str(data['comm_msg_info']['datetime'])
                        article_url = data['app_msg_ext_info']['content_url']
                        copyright = data['app_msg_ext_info']['copyright_stat']

                        if copyright != 11:  # 这里只生成原创文章
                            continue

                        copyright = '原创' if copyright == 11 else '非原创'
                        self.count = self.count + 1
                        title = '{}_{}_{}_{}'.format(self.gzh_name, copyright, article_time, title)
                        print(title)
                        self.request_artiacl_html(title, article_url)
                    except Exception as e:
                        print(e.args)
                        continue

                time.sleep(1)
                self.offset = all_datas['next_offset']  # 下一页的偏移量
                self.request_data()
            else:
                exit('数据抓取完毕！')

        else:
            exit('数据抓取出错:' + all_datas['errmsg'])

    def time_long_to_str(self, time_stamp):
        """把long类型的时间转换成字符串形式"""
        timeArray = time.localtime(time_stamp)
        strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
        return strTime[:10]

    def request_artiacl_html(self, title, url):
        """
         根据文章的url地址获取他的网页源代码，来拼接出pdf
        """
        try:
            response = requests.get(url=url, headers=self.headers)  # 一定要加headers，规范写法，就像过马路一样穿红灯有时没事，有时要命！
            if response.status_code == 200:  # 注意：这里一定要做200判断，
                self.creat_pdf_file(title,
                                    self.create_article_content(url, response.text))
        except Exception as e:
            print(sys._getframe().f_code.co_name)
            print(e.args)
            raise

    def create_article_content(self, url, text):
        """文章内容"""
        str = '<span style="font-size:30px"><a href = "{}">点击查看公众号原文</a></span>'.format(
            url) + text.replace('data-src', 'src')
        return str

    def creat_pdf_file(self, title, html_content):
        html = 'tmp.html'  # 这里是存放临时html文件
        with open(html, 'w', encoding='utf-8') as f:  # 点击open函数查看用法，这里是写入不要搞错了
            f.write(html_content)

        try:
            output_file = 'D:/gzh2/{}.pdf'.format(title)
            if not os.path.exists(output_file):  # 过滤掉重复文件
                pdfkit.from_file(html, output_file, configuration=self.config,
                                 )  # 注意这里需要配置一下wkhtmltopdf
        except Exception as e:
            print(sys._getframe().f_code.co_name)
            print(e)
        finally:
            os.remove(html)


if __name__ == '__main__':
    gzh = wx_gzh()
    gzh.request_data()
