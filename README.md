# python_project
自己学习python编写的各个小项目
以后计划pyqt5编写几个图形化界面，然后做几个网页
目前比较成熟的小项目：
- 1、1024爬虫，在crawl_down_pic_1024文件夹下，爬取盖区图片，记录前100页的信息，并多线程下载图片，详细功能后续补充，或直接看源码
- 2、学习强国app自动刷分，在phone文件夹下qiangguo_fuzhu文件夹下，qiangguoshuafen，可自动完成手机上app的刷分，依赖于pytesseract、uiautomator2、fuzzywuzzy，需按照对应库或文件，安装办法可google

- 本项目如有任何问题，可直接联系我，微信号：jiajia172001

学习笔记
- 1、pyinstaller 坑。打包时候遇到错误No module named 'pkg_resources.py2_warn'，需要重新安装setuptools
pip uninstall setuptools
pip install setuptools
原因是setuptools低版本有bug
- 2、pyinstaller 打包后运行出错，出现Importing the numpy C-extensions failed.
Original error was: DLL load failed while importing _multiarray_umath: 找不到指定的模块。
这是因为pyinstaller 自动打包时候会漏掉numpy的关键依赖文件，把
C:\Users\jiaji\AppData\Local\Programs\Python\Python38\Lib\site-packages\numpy
下面的.libs文件夹拷贝到。。。。。\dist\ceshi_1\numpy下面，就可以正常运行
