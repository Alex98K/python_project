import datetime
import os
import xlrd
import xlwt
from tijiaoxitong import SubmitSystem


def date_to_chuo(cell_value, format='%m/%d'):
    temp = datetime.datetime.strptime(str(cell_value), format)
    if temp.year == 1900:
        temp = temp.replace(year=2020)
    print(temp)
    today = datetime.datetime.strptime('1899-12-30', '%Y-%m-%d')
    return (temp-today).days


def excel_data(sheet_1):
    merge_cell = {}
    for item in sheet_1.merged_cells:
        for row in range(item[0], item[1]):
            for col in range(item[2], item[3]):
                if (row, col) != (item[0], item[2]):
                    merge_cell[(row, col)] = (item[0], item[2])
    data_1 = []
    for i in range(3, sheet_1.nrows):
        row_val = sheet_1.row_values(i)
        if row_val[0] == '总计':
            break
        for j_1 in range(sheet_1.ncols):
            if merge_cell.get((i, j_1)):
                row_val[j_1] = sheet_1.cell_value(*merge_cell.get((i, j_1)))
            else:
                row_val[j_1] = sheet_1.row_values(i)[j_1]
            if row_val[j_1] == "/":
                row_val[j_1] = ""
        if row_val[1] == "":
            break
        # print(row_val[1])
        try:
            xlrd.xldate_as_tuple(row_val[1], 0)
        except TypeError:
            try:
                row_val[1] = date_to_chuo(row_val[1], '%Y/%m/%d')
            except ValueError:
                pass
            try:
                row_val[1] = date_to_chuo(row_val[1], '%m/%d')
            except ValueError:
                pass
            try:
                row_val[1] = date_to_chuo(row_val[1], '%m-%d')
            except ValueError:
                pass
            try:
                row_val[1] = date_to_chuo(row_val[1], '%Y-%m-%d')
            except ValueError:
                pass
            try:
                row_val[1] = date_to_chuo(row_val[1], '%m.%d')
            except ValueError:
                pass
            try:
                row_val[1] = date_to_chuo(row_val[1], '%Y.%m.%d')
            except ValueError:
                pass
            try:
                row_val[1] = date_to_chuo(row_val[1], '%m月%d日')
            except ValueError:
                pass
            try:
                row_val[1] = date_to_chuo(row_val[1], '%Y年%m月%d日')
            except ValueError:
                pass
        except Exception:
            raise ('日期格式不对')
        if isinstance(row_val[10], float):
            row_val[10] = int(row_val[10])
        if isinstance(row_val[6], float):
            row_val[6] = int(row_val[6])
        if isinstance(row_val[7], float):
            row_val[7] = int(row_val[7])
        if isinstance(row_val[9], float) or isinstance(row_val[9], int):
            p = list(str(int(row_val[9])))
            p.insert(3, "-")
            row_val[9] = "".join(p)
        elif isinstance(row_val[9], str) and "-" not in row_val[9]:
            p = list(row_val[9])
            p.insert(3, "-")
            row_val[9] = "".join(p)
        if not isinstance(row_val[3], str):
            print("有航班号没有加二字码")
            raise
        data_1.append(row_val)
    return data_1


def write_excel(file_name1, data2):
    today = datetime.date.today()
    yesterday = today - datetime.timedelta(days=1)
    today_date = str(int(str(today)[5:7]))+"月"+str(int(str(today)[8:]))+"日"
    yesterday_date = str(int(str(yesterday)[5:7]))+"月"+str(int(str(yesterday)[8:]))+"日"
    book1 = xlwt.Workbook()
    sheet1 = book1.add_sheet("sheet1")

    style1 = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = "SimSun"  # 宋体
    font.height = 20 * 20  # 字体大小为11，字体大小的基本单位是20.
    font.bold = True  # 设置字体为不加粗
    style1.font = font
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style1.borders = borders
    style1.alignment.horz = 0x02
    # 水平居中
    style1.alignment.vert = 0x01
    # 垂直居中

    style2 = xlwt.XFStyle()
    font = xlwt.Font()
    font.name = "SimSun"  # 宋体
    font.height = 16 * 20  # 字体大小为11，字体大小的基本单位是20.
    font.bold = False  # 设置字体为不加粗
    style2.font = font
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style2.borders = borders
    style2.alignment.horz = 0x02
    # 水平居中
    style2.alignment.vert = 0x01
    # 垂直居中
    # 1-自动换行,0-不自动换行
    style2.alignment.wrap = 1
    # 缩小字体填充
    style2.alignment.shri = 0

    style3 = xlwt.XFStyle()
    style3.num_format_str = 'm月d日'
    font = xlwt.Font()
    font.name = "SimSun"  # 宋体
    font.height = 16 * 20  # 字体大小为11，字体大小的基本单位是20.
    font.bold = False  # 设置字体为不加粗
    style3.font = font
    borders = xlwt.Borders()
    borders.left = 1
    borders.right = 1
    borders.top = 1
    borders.bottom = 1
    style3.borders = borders
    style3.alignment.horz = 0x02
    # 水平居中
    style3.alignment.vert = 0x01
    # 垂直居中
    # 1-自动换行,0-不自动换行
    style3.alignment.wrap = 1
    # 缩小字体填充
    style3.alignment.shri = 0

    sheet1.col(0).width = 11 * 256
    sheet1.col(1).width = 14 * 256
    sheet1.col(2).width = 22 * 256
    sheet1.col(3).width = 18 * 256
    sheet1.col(4).width = 14 * 256
    sheet1.col(5).width = 14 * 256
    sheet1.col(6).width = 14 * 256
    sheet1.col(7).width = 14 * 256
    sheet1.col(8).width = 14 * 256
    sheet1.col(9).width = 24 * 256
    sheet1.col(10).width = 14 * 256
    sheet1.col(11).width = 14 * 256
    sheet1.col(12).width = 24 * 256
    sheet1.col(13).width = 14 * 256
    sheet1.col(14).width = 14 * 256

    sheet1.write_merge(0, 0, 0, 14, f"华北地区机场疫情防控人员物资航空运输统计表（{yesterday_date}15点-{today_date}15点）", style1)
    sheet1.write_merge(1, 2, 0, 0, "序号", style2)
    sheet1.write_merge(1, 2, 1, 1, "日期", style2)
    sheet1.write_merge(1, 2, 2, 2, "航空公司", style2)
    sheet1.write_merge(1, 2, 3, 3, "航班号", style2)
    sheet1.write_merge(1, 2, 4, 4, "始发站", style2)
    sheet1.write_merge(1, 2, 5, 5, "目的站", style2)
    sheet1.write(1, 6, "医护人员", style2)
    sheet1.write(2, 6, "（名）", style2)
    sheet1.write_merge(1, 1, 7, 8, "行李", style2)
    sheet1.write(2, 7, "数量（件）", style2)
    sheet1.write(2, 8, "重量（公斤）", style2)
    sheet1.write_merge(1, 1, 9, 12, "货物", style2)
    sheet1.write(2, 9, "运单号", style2)
    sheet1.write(2, 10, "数量（件）", style2)
    sheet1.write(2, 11, "重量（公斤）", style2)
    sheet1.write(2, 12, "品名", style2)
    sheet1.write_merge(1, 2, 13, 13, "是否包机", style2)
    sheet1.write_merge(1, 2, 14, 14, "备注", style2)
    row_in = 0
    for row_in, row_val in enumerate(data2):
        for col_in, col_val in enumerate(row_val):
            if col_in == 0:
                sheet1.write(row_in+3, 0, row_in+1, style2)
            elif col_in == 1:
                sheet1.write(row_in + 3, col_in, col_val, style3)
            else:
                sheet1.write(row_in+3, col_in, col_val, style2)
    row_in = row_in + 3
    sheet1.write(row_in+1, 0, "总计", style2)
    sheet1.write(row_in+1, 1, "--", style2)
    sheet1.write(row_in+1, 2, "--", style2)
    sheet1.write(row_in+1, 3, "--", style2)
    sheet1.write(row_in+1, 4, "--", style2)
    sheet1.write(row_in+1, 5, "--", style2)
    sheet1.write(row_in+1, 9, "--", style2)
    sheet1.write(row_in+1, 12, "--", style2)
    sheet1.write(row_in+1, 13, "--", style2)
    sheet1.write(row_in+1, 14, "--", style2)
    sheet1.write_merge(row_in+2, row_in+2, 0, 1, "报送单位：", style2)
    sheet1.write_merge(row_in+2, row_in+2, 2, 6, "华北局", style2)
    sheet1.write(row_in+2, 7, "报送人：", style2)
    sheet1.write(row_in+2, 8, "王海茏", style2)
    sheet1.write(row_in+2, 9, "联系方式：", style2)
    sheet1.write_merge(row_in+2, row_in+2, 10, 11, "64593776", style2)
    sheet1.write(row_in+2, 12, "报送时间：", style2)
    sheet1.write_merge(row_in+2, row_in+2, 13, 14, str(today), style2)
    book1.save(file_name1)


if __name__ == '__main__':
    file_name = "华北地区疫情防控人员物资航空运输统计表.xls"
    path = os.path.abspath(os.path.dirname(__file__))
    files = os.listdir(path)
    files1 = files.copy()
    for j in files1:
        if os.path.isdir(os.path.join(path, j)):
            files.remove(j)
            continue
        if "xls" not in j:
            files.remove(j)
    if file_name in files:
        files.remove(file_name)
    data = []
    print(files)
    for f in files:
        book = xlrd.open_workbook(os.path.join(path, f))
        sheet = book.sheet_by_index(0)
        data1 = excel_data(sheet)
        data.extend(data1)
        os.remove(f)
    print(data)
    if data:
        write_excel(file_name, data)
        p = SubmitSystem()
        p.main(os.path.join(path, file_name))
