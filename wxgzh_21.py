import requests

import time
import json
import os
import pdfkit


class mp_spider(object):

    def __init__(self):
        self.config = pdfkit.configuration(wkhtmltopdf='C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe')
        self.offset = 0
        self.count = 0
        self.common_msg = 'https://mp.weixin.qq.com/mp/appmsg_comment?action=getcomment&scene=0&__biz=MjM5MTQ4NjA3Nw==&appmsgid=2459679838&idx=1&comment_id=858146915022700544&offset=0&limit=100&uin=NjY2Mzg5MDY0&key=8dcddb6b0d83f29d407459739f566e1dade10ef3321de42925d6196cb12c49c0623ec3bd87834beea22e0204866c50087e68e90f6f8dd9335ba88785ae3a934d5727a1bae93c81daf022f87f60d91a46&pass_ticket=VZT065Rmh4IAV%25252Fae009Bi4ZhNVZfiFy70LmY3SpkbTJnPN04iVB9Nyi7Eyg0q6vt&wxtoken=777&devicetype=Windows%26nbsp%3B10&clientversion=62060833&appmsg_token=1013_KqX2BoHRm3ZdtT6YyywfGkhUW-_EQhtvvrUGxHsvkOlKy3gc1QIOXeYC5K2DK9sTNjC7rl0GPr8y4oAD&x5=0&f=json'
        self.base_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=getmsg&__biz=MzAwMjQwODIwNg==&f=json&offset={}&count=10&is_ok=1&scene=124&uin=MTIyOTkzMzgyMA%3D%3D&key=7cabb994f4d85a88ad37c1ec41ddde6234e76a1f1e69b178052bc99ccdf724f77700b28cea9e242cc98e517bd2537122fdc7a65a601e36f438b33e31e183f64dd9519beed36d892cc0a31855f1c649d6&pass_ticket=n6xnvQjzn4yfkjScc%2FSoVi4SkEgzf4z0airW6Ue14zIDNH98t%2Fr62k2KszUJ1qNv&wxtoken=&appmsg_token=960_mNI0W0CuVRuEpG7GsxB7f7pUUrO2CWW_iib4ww~~&x5=0&f=json'
        self.cookie = 'rewardsn=; wxtokenkey=777; wxuin=666389064; devicetype=Windows10; version=62060833; lang=zh_CN; pass_ticket=VZT065Rmh4IAV/ae009Bi4ZhNVZfiFy70LmY3SpkbTJnPN04iVB9Nyi7Eyg0q6vt; wap_sid2=CMiU4b0CElxwNHk1bk9lLWR4V3ZzUjlWbXh3SXM0NFUwbm5MS25oRmdYY1BXdlIzalUwOXJnYmZJaTc4bUkzZE5ndTM2UU9nS29DVXhRZ0FOak03SEpLbVc0RzlIdlVEQUFBfjC1wJzoBTgNQJVO'
        self.referer = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz=MzU0NjcwOTYzOQ==&scene=124&uin=NjY2Mzg5MDY0&key=6ff676ea8e4091fdf15de82d16de6e605c753ab9d5acfd34bc90f2f5eadc5febf214ce232bc10cbb4fe376425ccb6842a359bcdde73061d7ba547b2dce8098f9685888cad250b5f5da75c5b600bd0a71&devicetype=Windows+10&version=62060833&lang=zh_CN&a8scene=7&pass_ticket=VZT065Rmh4IAV%2Fae009Bi4ZhNVZfiFy70LmY3SpkbTJnPN04iVB9Nyi7Eyg0q6vt&winzoom=1'

        self.headers = {
            'Host': 'mp.weixin.qq.com',
            'Connection': 'keep-alive',
            'Accept': '*/*',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.884.400 QQBrowser/9.0.2524.400',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': self.referer,
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-us;q=0.6,en;q=0.5;q=0.4',
            'Cookie': self.cookie
        }

    def request_data(self):
        response = requests.get(self.base_url.format(self.offset), headers=self.headers)
        if 200 == response.status_code:
            self.parse_data(response.text)

    def parse_data(self, response_data):
        all_datas = json.loads(response_data)
        if 0 == all_datas['ret']:
            if 1 == all_datas['can_msg_continue']:
                summy_datas = all_datas['general_msg_list']
                print(summy_datas)
                datas = json.loads(summy_datas)['list']
                for data in datas:
                    try:
                        title = data['app_msg_ext_info']['title']
                        title_child = data['app_msg_ext_info']['digest']
                        article_url = data['app_msg_ext_info']['content_url']
                        cover = data['app_msg_ext_info']['cover']
                        copyright = data['app_msg_ext_info']['copyright_stat']
                        copyright = '原创文章_' if copyright == 11 else '非原创文章_'
                        self.count = self.count + 1
                        print('第【{}】篇文章'.format(self.count), copyright, title, title_child, article_url, cover)
                    #   print('{}_{}_{}'.format(copyright, title,)

                    except:
                        continue

                time.sleep(3)
                self.offset = all_datas['next_offset']  # 下一页的偏移量
                self.request_data()
            else:
                exit('数据抓取完毕！')
        else:
            exit('数据抓取出错:' + all_datas['errmsg'])


if __name__ == '__main__':
    d = mp_spider()
    d.request_data()
