import xlrd
import csv

# From http://stackoverflow.com/questions/9884353/xls-to-csv-convertor
#
# Used to convert 2007 and 2008 column lookup tables to CSV because they
# are only supplied as XLS.

wb = xlrd.open_workbook('merge_5_6.xls')
sh = wb.sheet_by_name('merge_5_6')
your_csv_file = open('merge_5_6.csv', 'wb')
wr = csv.writer(your_csv_file, quoting=csv.QUOTE_ALL)

for rownum in xrange(sh.nrows):
    wr.writerow(sh.row_values(rownum))

your_csv_file.close()
