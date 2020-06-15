import requests
from lxml import etree
import xlwt
import time

haders = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"}
all_jieguo = []
data = xlwt.Workbook()
table = data.add_sheet('tiku')
j = 0
for i in range(1, 1925):
    try:
        url_question = "http://www.okkkj.cn/q-{}.html".format(i)
        res_answer = requests.get(url_question, headers=haders)
        html_answer = etree.HTML(res_answer.content.decode())
        question = html_answer.xpath('//div[@class="container questiondetail"]//div[@class="col-sm-9"]//text()')
        question = "".join(question)
        question = question.replace(" ", "").replace("\r", "").replace("\n", "")
        if not question:
            question = html_answer.xpath('//div[@class="row question-des"]//div[@class="col-sm-12"]/p[1]/text()')
        answer = html_answer.xpath('//div[@class="row question-des"]//span[contains(@style,"background-color")]//text()')
        if not answer:
            answer = html_answer.xpath('//div[@class="row question-des"]//div[@class="col-sm-12"]/p[2]/text()')
        answer = "".join(answer)
        answer_all = html_answer.xpath('//div[@class="row question-des"]//span[contains(@style,"font")]//text()')
        # jieguo = [question, answer_all, "".join(answer), i]
        if question or answer or answer_all:
            # all_jieguo.append(jieguo)
            print("找到的问题是\n", question)
            print("找到的全部答案是\n", answer_all)
            print("找到的答案是\n", answer)
            table.write(j, 0, question)
            table.write(j, 1, str(answer_all))
            table.write(j, 2, answer)
            table.write(j, 3, i)
            j += 1
            # data.save('tiku1.xls')
        time.sleep(1)
    except Exception as e:
        pass
# print(all_jieguo)
data.save('tiku.xls')
