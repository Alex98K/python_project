from win32com import client as wc
import os


def doc2docx(title, flag=None):
    title.replace('.doc', '').replace('.docx', '')
    word = wc.Dispatch('Word.Application')
    path = os.path.abspath(os.path.dirname(__file__))
    doc = word.Documents.Open('{}/{}.doc'.format(path, title))  # 目标路径下的文件
    doc.SaveAs('{}/{}.docx'.format(path, title), 12, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
    doc.Close()
    word.Quit()
    if flag is None:
        os.remove('{}/{}.doc'.format(path, title))


def docx2doc(title, flag=None):
    title.replace('.doc', '').replace('.docx', '')
    word = wc.Dispatch('Word.Application')
    path = os.path.abspath(os.path.dirname(__file__))
    doc = word.Documents.Open('{}/{}.docx'.format(path, title))  # 目标路径下的文件
    doc.SaveAs('{}/{}.doc'.format(path, title), 0, False, "", True, "", False, False, False, False)  # 转化后路径下的文件
    doc.Close()
    word.Quit()
    if flag is None:
        os.remove('{}/{}.docx'.format(path, title))


if __name__ == '__main__':
    text = '2'
    doc2docx(text, flag=2)
    # docx2doc(title)
