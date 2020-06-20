# -*- coding: utf-8 -*-
import requests
import pytesseract
import cv2
import re
from requests_toolbelt.multipart.encoder import MultipartEncoder
from lxml import etree
import xlrd


class SubmitSystem(object):
    # 系统中新建环境变量TESSDATA_PREFIX，为C:\Program Files\Tesseract-OCR\tessdata
    # 重写tesseract.exe启动位置，无需设置环境变量
    pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

    # login_url = 'http://123.206.55.106:8066/danger/admin/login.jsp'
    # main_url = 'http://123.206.55.106:8066/danger/admin/main.action'
    check_url = 'http://123.206.55.106:8066/danger/admin/check.action'
    # data_url = 'http://123.206.55.106:8066/danger/danger/testt/collectionin.action'
    captcha_url = 'http://123.206.55.106:8066/danger/jcaptcha.jpg'
    # daoru_url = 'http://123.206.55.106:8066/danger/danger/testt/collectioninDaoru.action'
    submit_url = 'http://123.206.55.106:8066/danger/danger/testt/collectionDaoru.action'
    sure_url = 'http://123.206.55.106:8066/danger/danger/testt/collectiongl_save.action'
    list_url = 'http://123.206.55.106:8066/danger/danger/testt/collectionin-list.action'
    update_data_xpath = "//tr[@class='tfoot']/td[1]"


    User_Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36'
    Accept_Encoding = 'gzip, deflate'
    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    header1 = {'User-Agent': User_Agent, 'Accept-Encoding': Accept_Encoding, 'Accept': Accept,
               'Connection': 'keep-alive'}

    def denglu_session(self):
        while True:
            ses = requests.Session()
            captcha_pic = ses.get(self.captcha_url, headers=self.header1)
            with open('1.jpg', 'wb') as f:
                f.write(captcha_pic.content)
            pp = cv2.imread('1.jpg', 1)
            captcha_text = pytesseract.image_to_string(pp)
            # captcha_text = str(input('验证码：'))
            data = {'item.userName': 'hbglj', 'item.passwd': 'safety', 'jcaptcha': captcha_text}
            r = ses.post(self.check_url, data=data)
            if not re.findall(r'验证码错误', r.text):
                break
        return ses

    def tijiao_file(self, ses, file_path):
        # 请求头必须包含Content-Type: multipart/form-data; boundary=${bound}
        # 这里也可以自定义boundary
        header2 = self.header1
        multipart_encoder = MultipartEncoder(
            fields={'fileaj': ('华北地区疫情防控人员物资航空运输统计表.xls', open(file_path, 'rb'), 'multipart/form-data')})  # 这里根据需要进行参数格式设置
        header2['Content-Type'] = multipart_encoder.content_type
        try:
            ses.post(self.submit_url, data=multipart_encoder, headers=header2, stream=True)
            return True
        except Exception:
            return False

    def yanzheng_data(self, ses, file_path):
        yanzheng_html = ses.get(self.list_url, headers=self.header1)
        if yanzheng_html.status_code == 404:
            print("获取验证数据错误，404")
            return False
        data_yeshu = etree.HTML(yanzheng_html.text).xpath(self.update_data_xpath)[0]
        res = re.search(r'\d+', data_yeshu.text).group()
        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)
        if int(res) == sheet.nrows - 5:
            return True
        else:
            return False

    def main(self, file_path):
        ses = self.denglu_session()
        print("已经登录，准备提交文件")
        self.tijiao_file(ses, file_path)
        print("提交完毕文件，准备验证是否有数据缺失")
        if self.yanzheng_data(ses, file_path):
            print('上传数据没有问题，进行提交确认')
            ses.get(self.sure_url, headers=self.header1)
            print('已经提交确认，完成工作')
        else:
            print('上传数据有缺失')
        ses.close()


if __name__ == '__main__':
    p = SubmitSystem()
    p.main(file_path = '/transport_afernoon/华北地区疫情防控人员物资航空运输统计表.xls')
