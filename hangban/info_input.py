import xlrd, pymysql, os

if (p := input('airport or airline ?\n')) == 'airport':
    title = (
    'IATA', 'ICAO', 'airport_eng', 'airport_chi', 'guan', 'province', 'country_id', 'country_chi', 'airport_style',
    'city')
    sheet_name = 'airport'
    table_name = 'airport_info'
elif p == 'airline':
    title = (
    'IATA', 'ICAO', 'airline_eng', 'airline_chi', 'airline_airport', 'chi_simple', 'airline_style', 'country', 'logo',
    'guan')
    sheet_name = 'airline'
    table_name = 'airline_info'
else:
    raise Exception('输入错误')


path_start = os.path.abspath(os.path.dirname(__file__))
title_db = str(tuple(title)).replace("\'", "")
db = pymysql.connect(host="localhost", user="root", passwd="jiajia0611", db="ceshi")
cur = db.cursor()
book = xlrd.open_workbook(path_start + '/数据库设计文档/info.xlsx')
sheet = book.sheet_by_name(sheet_name)
for j in range(1, sheet.nrows):
    p = str(tuple(sheet.row_values(j)))
    print(p)
    sql = "insert ignore into %s %s values %s" % (table_name, title_db, p)
    cur.execute(sql)
db.commit()
cur.close()
db.close()
