import pymysql
import xlrd
import re
import settings
import os
import shutil
from collections import Counter


def _start_cube(sheets):
    # 找到日期或运行日所在行列数
    start_row = None
    start_col = None
    for j in range(0, sheets.ncols):
        for i in range(0, sheets.nrows):
            if sheets.cell(i, j).value == "运行日" or sheets.cell(i, j).value == "日期":
                start_row = i
                start_col = j
                break
            else:
                continue
        if start_col is not None:
            break
    # print("数据表开始于{}行{}列（日期或执行日所在单元格）".format(start_row, start_col))
    return start_row, start_col


def _title_name_clean(sheets, start_row, start_col):
    # 标题数据清理
    title = [re.sub(r'text:|\n|\'', '', str(i)) for i in sheets.row_values(start_row, start_colx=start_col)]
    title_db = []
    pass_col = []
    for col, i in enumerate(title):
        try:
            title_db.append(settings.field_name[i])
        except KeyError:
            print('******跳过第{}-{}这一列******'.format(col, i))
            pass_col.append(col)
    title_db.append('In_Out_Sign')
    title_len = len(title_db)
    title_db = str(tuple(title_db)).replace("\'", "")
    # print(title_db)
    return title_db, pass_col, title_len


def _new_row(sheets, row_num, start_col, pass_col, in_out_logo):
    # 清洗数据，格式化每一行的数据，以便于可以录入数据库
    pattern = re.compile(r'text:|\\n|\'|number:|empty:')
    if pass_col:
        p = sheets.row_values(row_num, start_colx=start_col)
        for j in [p[i] for i in pass_col]:
            p.remove(j)
        row_tep = p
    else:
        row_tep = sheets.row_values(row_num, start_colx=start_col)
    row = [re.sub(pattern, '', str(j).replace("\'\'", "NULL").replace("：", ":")) for j in row_tep]
    rpw = []
    for j in row:
        if not j:
            j = None
        rpw.append(j)
    rpw.append(in_out_logo)
    # return str(tuple(row)).replace("\'\'", "NULL").replace("：", ":")
    # print(temp)
    return tuple(rpw)


def _sql_exe(cur, sql):
    # 执行sql语句
    try:
        cur.execute(sql)
    except Exception as e:
        print("下面的sql语句没有成功\n", sql)
        print("出错的原因是：", e)


def update_data(db, cur, table_name='hangban_pek'):
    update_sql = ['Closing_cabin_door=Closing_cargo_door where Closing_cabin_door is null and in_out_sign="出港" ',
                  'Closing_cargo_door=Closing_cabin_door where Closing_cargo_door is null and in_out_sign="出港" ',
                  'RDY_time=GREATEST(Closing_cabin_door, Closing_cargo_door) where RDY_time is null AND in_out_sign="出港"',
                  'company=left(flight_nb,2) where company is null',
                  'Plan_Station=timestampdiff(minute,Planned_arrival,Planned_depart) where Plan_Station is null',
                  'ASAT=Actual_depart where ASAT is null and in_out_sign="出港"'
                  ]
    # 原计划按年度分为不同机场不同年度表格，现在计划一个机场一个表，就不用之前的方法了
    # update_sql_all = ['update {} set '.format(table_name + str(k)) + i for k in res for i in update_sql]
    update_sql_all = ['update {} set '.format(table_name) + k for k in update_sql]
    for j in update_sql_all:
        _sql_exe(cur, j)
        print('update更新完毕\n {}'.format(j))
    db.commit()


def import_data(db, cur, table_name='hangban_pek'):
    path = './待导入的航班数据'
    path_dst = ''
    excel_files = os.listdir(path)
    # res = []
    for j in excel_files:
        # 读取excel文件
        book = xlrd.open_workbook(os.path.join(path, j))
        book_sheet_names = book.sheet_names()
        print("{} excel中共有以下数据表 ".format(j), book_sheet_names)
        for i in book_sheet_names:
            if '进港' in i and '出' not in i:
                in_out_logo = '进港'
            elif '出' in i and '进' not in i:
                in_out_logo = '出港'
            else:
                raise Exception('excel表格工作页读取有误')
            sheets = book.sheet_by_name(i)
            print("{}数据表共有{}行和{}列".format(i, sheets.nrows, sheets.ncols))
            start_row, start_col = _start_cube(sheets)
            title_db, pass_col, title_len = _title_name_clean(sheets, start_row, start_col)
            # 从表格中获取日期，然后截取前四位，然后计数获得最多的，作为数据库表格的后四位，（暂时不使用）
            last = Counter([str(k)[:4] for k in sheets.col_values(start_col, start_row + 1)]).most_common(1)[0][0]
            # res.append(last)
            # print('插入hangban{}表中'.format(last))
            # table_name_in = table_name + last
            path_dst = './旧数据/{}'.format(last)
            # for k in range(start_row + 1, sheets.nrows):  # 原来的单条插入数据，已作废
            #     sql = "insert ignore into %s %s values %s" % (table_name, title_db, _new_row(
            #         sheets, k, start_col, pass_col, in_out_logo))
            #     _sql_exe(cur, sql)
            data = tuple(
                (_new_row(sheets, k, start_col, pass_col, in_out_logo)) for k in range(start_row + 1, sheets.nrows))
            sql = "insert ignore into {} {} values {}".format(table_name, title_db,
                                                              '(' + '%s,' * (title_len - 1) + '%s)')
            cur.executemany(sql, data)
        db.commit()
        shutil.move(os.path.join(path, j), os.path.join(path_dst, j))
    # return list(set(res))  # 返回所插入表的编号，例如插入了[2019,2020]表


def exempt_data(db, cur, table_name='hangban_pek'):
    """ 导入豁免数据，excel格式，第一列
    :param db:
    :param cur:
    :param table_name:
    :return:
    """
    path = './待导入的豁免数据'
    path_dst = './旧数据/豁免数据'
    excel_files = os.listdir(path)
    for j in excel_files:
        # 读取excel文件
        book = xlrd.open_workbook(os.path.join(path, j))
        book_sheet_names = book.sheet_names()
        print("待豁免数据导入：{} excel中共有以下数据表 ".format(j), book_sheet_names)
        for i in book_sheet_names:
            sheets = book.sheet_by_name(i)
            # 从表格中获取日期，然后截取前四位，然后计数获得最多的，作为数据库表格的后四位，暂时不用了
            # last = Counter([k[:4] for k in sheets.col_values(0)]).most_common(1)[0][0]
            # table_name += str(last)
            data = []
            for c in range(1, sheets.nrows):
                p = sheets.row_values(c)
                # sql = f"update {table_name} set In_Out_Sign='豁免' where date='{xlrd.xldate_as_datetime(p[0], 0)}' and Flight_nb='{p[1]}'"
                # _sql_exe(cur, sql)
                data.append(tuple((xlrd.xldate_as_datetime(p[0], 0), p[1])))
            sql = "update {} set In_Out_Sign='豁免' where date=%s and Flight_nb=%s".format(table_name, data)
            cur.executemany(sql, data)
        db.commit()
        shutil.move(os.path.join(path, j), os.path.join(path_dst, j))


def change_time_data(db, cur, table_name='hangban_pek'):
    """
    导入调时数据，excel格式：第一列执行日期，第二列航班号，第三列改后的STD时间
    :param db:
    :param cur:
    :param table_name:
    :return:
    """
    path = './待导入的调时数据'
    path_dst = './旧数据/调时数据'
    excel_files = os.listdir(path)
    for j in excel_files:
        # 读取excel文件
        book = xlrd.open_workbook(os.path.join(path, j))
        book_sheet_names = book.sheet_names()
        print("调时数据导入：{} excel中共有以下数据表 ".format(j), book_sheet_names)
        for i in book_sheet_names:
            sheets = book.sheet_by_name(i)
            for c in range(1, sheets.nrows):
                p = sheets.row_values(c)
                sql = f"update {table_name} set Planned_depart='{xlrd.xldate_as_datetime(p[2], 0)}' where date='{xlrd.xldate_as_datetime(p[0], 0)}' and Flight_nb='{p[1]}' and in_out_sign='出港' "
                _sql_exe(cur, sql)
        db.commit()
        shutil.move(os.path.join(path, j), os.path.join(path_dst, j))


def main():
    db = pymysql.connect(host="localhost", user="root", passwd="jiajia0611", db="ceshi")
    cur = db.cursor()
    import_data(db, cur)  # 导入数据进入数据库
    update_data(db, cur)  # 按照设定的语句，刷新数据
    change_time_data(db, cur)  # 按照设定的语句，刷新计划离港时间数据
    exempt_data(db, cur)  # 导入豁免数据
    cur.close()
    db.close()


if __name__ == '__main__':
    main()
