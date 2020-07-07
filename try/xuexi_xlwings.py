import xlwings as xw

wb = xw.Book("1.xlsx")

sht = wb.sheets["登记"]
sht.range('A1').value = [[1,2],[3,4]]
pp = sht.range('A1').expand().value

print(pp)
