import xlrd
import csv

# From http://stackoverflow.com/questions/9884353/xls-to-csv-convertor
#
# Used to convert 2007 and 2008 column lookup tables to CSV because they
# are only supplied as XLS.

wb = xlrd.open_workbook('merge_5_6_final.xls')
sh = wb.sheet_by_name('merge_5_6')
your_csv_file = open('merge_5_6.csv', 'wb')
wr = csv.writer(your_csv_file)

for rownum in xrange(sh.nrows):
    rowvals = [unicode(s).encode('utf8') for s in sh.row_values(rownum)]
    wr.writerow(rowvals)

your_csv_file.close()
