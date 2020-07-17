import win32com.client
from time import sleep
from selenium import webdriver

# selenium 实验
# driver = webdriver.Edge()
# 实例化一个启动参数对象
# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# 启动浏览器
# driver = webdriver.Chrome(r'D:\python_project\chromedriver.exe', options=options)
# driver.implicitly_wait(10) # seconds
# driver.get('https://cl.2yi.xyz/thread0806.php?fid=16')
# o = driver.find_element_by_xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a//text()")
# hh = etree.HTML(driver.page_source)
# print(hh)
# driver.quit()
# print(hh.xpath("//tr[@class='tr3 t_one tac' and not(contains(@align,'middle'))]//h3/a//text()"))

# ************************************************************************************************

# 用win32com接口调用浏览器
url = 'https://cl.h8c.xyz/htm_data/2007/16/3984520.html'
iewindow = win32com.client.DispatchEx("InternetExplorer.Application")
print(iewindow.PATH)
nv = iewindow.Navigate(url)
iewindow.Visible = 0  # 1表示IE窗口显示，你可以换0试试
while True:
    if iewindow.ReadyState == 4 and str(iewindow.LocationURL) == url:
        break
    sleep(1)
doc = iewindow.document
body = doc.body
# doc.location.reload()
# print(doc.all.item('header').outerHTML)
# print(doc.all.item('atc_content').outerHTML)
doc.all.item('atc_content').value='908'
doc.all.item('Submit').click()

# body.querySelector("#main")
# print(doc.cookie)
# print(doc.characterSet)
# print(doc.implementation)
# print(doc.location)
# for k in doc.images:
# print(k.outerHTML)
# print(k.innerHTML)
# print(k.id)
# k.click()
# print(k.classList)
# print(k.attributes[0].name)
# print(doc.all['textarea'])
# for j in doc.images:
#     print(j.src)

#
# iewindow.Quit()  # 关闭该IE窗口
