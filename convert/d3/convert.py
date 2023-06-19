import csv

out = open('用户行为分析.csv', 'w', newline='')  # 要转成的.csv文件，先创建一个.csv文件
csv_writer = csv.writer(out, dialect='excel')

f = open("d1.txt", "r",encoding="utf8")
for line in f.readlines():
    line = line.replace(',', '\t')  # 将每行的逗号替换成空格
    list = line.split()  # 将字符串转为列表，从而可以按单元格写入csv
    csv_writer.writerow(list)