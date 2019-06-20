import os

import pdfkit
import requests


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
                        '<span style="font-size:30px"><a href = "{}">公众号原文地址</a></span><br>'.format(
                            url) + response.text.replace('data-src', 'src'))
                else:
                    continue
        except Exception as e:
            print(e.args)
        finally:
            self.creat_pdf_file('Python绿色通道')

    def creat_pdf_file(self, group_title):
        htmls = []  # 这里是存放html文件

        for index, file in enumerate(self.html_contents):
            html = '{}.html'.format(index)
            with open(html, 'w', encoding='utf-8') as f:  # 点击open函数查看用法，这里是写入不要搞错了
                f.write(file)

            htmls.append(html)

        try:
            output_file = 'D:/gzh/{}.pdf'.format(group_title)
            if not os.path.exists(output_file):  # 过滤掉重复文件
                pdfkit.from_file(htmls, output_file, configuration=self.config,
                                 )  # 注意这里需要配置一下wkhtmltopdf
        except Exception as e:
            print(e)
        finally:
            for html_file in htmls:  # 清除生成的html文件
                os.remove(html_file)

    pass


if __name__ == '__main__':
    gzh = wx_gzh()
    gzh.request_artiacl_content()
