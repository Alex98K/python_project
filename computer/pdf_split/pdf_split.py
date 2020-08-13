import PyPDF2


# 每两页分割为一个单独的pdf，然后保存
pdfFile = open('1.pdf', 'rb')
pdfReader = PyPDF2.PdfFileReader(pdfFile,  strict=False)
start_page = 1  # 从第一页开始
end_page = pdfReader.getNumPages() + 1  # 到文件最后一页
every_pages = 2  # 每两页生成一个新文件
for j in range(start_page, end_page, every_pages):
    page = pdfReader.getPage(j-1)  # 获取第0页
    page2 = pdfReader.getPage(j)  # 获取第0页
    # page3 = pdfReader.getPage(j+1)  # 获取第0页
    writer = PyPDF2.PdfFileWriter()  # 创建PDF写入的对象
    writer.addPage(page)
    writer.addPage(page2)
    # writer.addPage(page3)
    outputStream = open(f'temp/{j}.pdf', 'wb')  # 创建一个PDF文件
    writer.write(outputStream)  # 往文件写入PDF数据
    outputStream.close()
