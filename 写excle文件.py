# _*_coding:UTF-8 _*_
import xlwt
'''
workbook = xlwt.Workbook(encoding='utf-8')
worksheet = workbook.add_sheet('sheet1')
worksheet.write(0,0,'hello')
workbook.save('students.xls')
'''

# 创建workbook对象
workbook = xlwt.Workbook(encoding='utf-8')
# 创建工作表
worksheet = workbook.add_sheet('sheet1')
for i in range(0, 9):
    for j in range(0, i + 1):
        worksheet.write(i, j, "%d*%d=%d" % (i + 1, j + 1, (i + 1) * (j + 1)))
workbook.save('student.xle')
