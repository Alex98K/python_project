import datetime
import os

import numpy as np
import pandas as pd

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)
path = os.path.abspath(os.path.dirname(__file__))
files = os.listdir(path)
file_name = None
for j in files:
    if "防控物资" in j:
        file_name = j
    elif j not in ['transport_sum.py', 'info.xlsx', 'run.ps1']:
        os.remove(os.path.join(path, j))
if not file_name:
    raise FileNotFoundError
info = pd.read_excel(os.path.join(path, "info.xlsx"), sheet_name=[0, 1])
airport = pd.DataFrame(info[0]).iloc[:, [3, 4]]
airline = pd.DataFrame(info[1]).iloc[:, [0, 5]]
data = pd.DataFrame(
    pd.read_excel(os.path.join(path, file_name), sheet_name='汇总', skiprows=3, usecols=[i for i in range(1, 15)],
                  names=["日期", "航空公司", "航班号", "始发站", "目的站", "医护人员", "行李数量", "行李重量", "运单号",
                         "货物数量", "货物重量", "品名", "是否包机", "备注"]))
data = data[["日期", "航空公司", "航班号", "始发站", "目的站", "医护人员", "货物数量", "货物重量"]]
data["货物重量"] = pd.to_numeric(data["货物重量"], errors="coerce")
data["货物数量"] = pd.to_numeric(data["货物数量"], errors="coerce")
data["医护人员"] = pd.to_numeric(data["医护人员"], errors="coerce")
data["日期"] = pd.to_datetime(data["日期"], errors='ignore').dt.date
data["航班号"].astype(str, errors="ignore")

data["二字码"] = data["航班号"].str[:2]
data["二字码"] = data["二字码"].str.upper()
data["始发站"].replace(r"(\u673a\u573a)|(\u767d\u5854)|(\u9996\u90fd)|\s", "", inplace=True, regex=True)

res1 = pd.merge(data, airport, how="left", left_on="始发站", right_on="机场中文名")
res2 = pd.merge(res1, airline, how="left", left_on="二字码", right_on="航空公司二字码")
res = pd.merge(res2, airline, how="left", left_on="航空公司", right_on="航空公司二字码", suffixes=("_ap", "_cp"))
res["中文简称_ap"].fillna(value=res["中文简称_cp"], inplace=True)
res["中文简称_ap"].fillna(value=res["航空公司"], inplace=True)

res_a = res[res["管理局"] == "华北"]
res_a = res_a[["日期", "中文简称_ap", "机场中文名", "医护人员", "货物数量", "货物重量"]]
res_a.columns = ["日期", "公司简称", "始发机场", "医护人员", "货物数量(件)", "货物重量(吨)"]
res_a.fillna(value=0, inplace=True)

res_h = res[(res["管理局"] == "华北") & (res["日期"] == yesterday)]
res_h = res_h[["中文简称_ap", "机场中文名", "货物数量", "货物重量"]]
res_h.columns = ["公司简称", "始发机场", "货物数量(件)", "货物重量(吨)"]
res_h.fillna(value=0, inplace=True)

p1 = pd.DataFrame(
    pd.pivot_table(res_h, values=["货物数量(件)", "货物重量(吨)"], index=[u"始发机场"], fill_value=0, aggfunc=[np.sum],
                   margins=True, margins_name="合计"))
p1.columns = p1.columns.droplevel(0)
p1.reset_index()
p2 = pd.DataFrame(
    pd.pivot_table(res_h, values=["货物数量(件)", "货物重量(吨)"], index=[u"公司简称"], fill_value=0, aggfunc=[np.sum],
                   margins=True, margins_name="合计"))
p2.columns = p2.columns.droplevel(0)
p2.reset_index()
p1.sort_values(by=["货物重量(吨)"], inplace=True)
p2.sort_values(by=["货物重量(吨)"], inplace=True)
p1["货物重量(吨)"] = round(p1["货物重量(吨)"] / 1000, 2)
p2["货物重量(吨)"] = round(p2["货物重量(吨)"] / 1000, 2)

p3 = pd.DataFrame(
    pd.pivot_table(res_a, values=["医护人员", "货物数量(件)", "货物重量(吨)"], index=[u"始发机场"], fill_value=0,
                   aggfunc=[np.sum], margins=True, margins_name="合计"))
p3.columns = p3.columns.droplevel(0)
p3.reset_index()
p4 = pd.DataFrame(
    pd.pivot_table(res_a, values=["医护人员", "货物数量(件)", "货物重量(吨)"], index=[u"公司简称"], fill_value=0,
                   aggfunc=[np.sum], margins=True, margins_name="合计"))
p4.columns = p4.columns.droplevel(0)
p4.reset_index()
p3.sort_values(by=["货物重量(吨)", "货物数量(件)", "医护人员"], inplace=True)
p4.sort_values(by=["货物重量(吨)", "货物数量(件)", "医护人员"], inplace=True)
p3["货物重量(吨)"] = round(p3["货物重量(吨)"] / 1000, 2)
p4["货物重量(吨)"] = round(p4["货物重量(吨)"] / 1000, 2)

res_a['日期'] = res_a['日期'].astype(str)
p5 = pd.DataFrame(
    pd.pivot_table(res_a, values=["医护人员", "货物数量(件)", "货物重量(吨)"], index=["日期", "始发机场"], fill_value=0,
                   aggfunc=[np.sum], margins=True, margins_name="合计"))
p5.columns = p5.columns.droplevel(0)
p5.reset_index()
p6 = pd.DataFrame(
    pd.pivot_table(res_a, values=["医护人员", "货物数量(件)", "货物重量(吨)"], index=["日期", "公司简称"], fill_value=0,
                   aggfunc=[np.sum], margins=True, margins_name="合计"))
p6.columns = p6.columns.droplevel(0)
p6.reset_index()
p5["货物重量(吨)"] = round(p5["货物重量(吨)"] / 1000, 2)
p6["货物重量(吨)"] = round(p6["货物重量(吨)"] / 1000, 2)
p5_sum = p5.groupby(level='日期').sum()
p6_sum = p6.groupby(level='日期').sum()
p5_sum.index = pd.MultiIndex.from_arrays(
    [p5_sum.index.get_level_values(0) + '_小计', len(p5_sum.index) * [''], len(p5_sum.index) * [''],
     len(p5_sum.index) * ['']])
p6_sum.index = pd.MultiIndex.from_arrays(
    [p6_sum.index.get_level_values(0) + '_小计', len(p6_sum.index) * [''], len(p6_sum.index) * [''],
     len(p6_sum.index) * ['']])
p5_a = pd.concat([p5, p5_sum]).sort_values(by=["日期", "货物重量(吨)", "货物数量(件)", "医护人员"])
p6_a = pd.concat([p6, p6_sum]).sort_values(by=["日期", "货物重量(吨)", "货物数量(件)", "医护人员"])

writer1 = pd.ExcelWriter(os.path.join(path, f"华北地区机场始发运输物资情况-昨日{yesterday}.xls"), engine='xlwt')
writer2 = pd.ExcelWriter(os.path.join(path, f"华北地区始发运输物资情况.xls"), engine='xlwt')
p1.to_excel(writer1, sheet_name=f"昨日{yesterday}按机场分")
p2.to_excel(writer1, sheet_name=f"昨日{yesterday}按公司分")
p3.to_excel(writer2, sheet_name=f"全部按机场分-截止{yesterday}")
p4.to_excel(writer2, sheet_name=f"全部按公司分-截止{yesterday}")
p6_a.to_excel(writer2, sheet_name="全部按日期公司分")
p5_a.to_excel(writer2, sheet_name="全部按日期机场分")

writer1.save()
writer2.save()

os.remove(os.path.join(path, file_name))
