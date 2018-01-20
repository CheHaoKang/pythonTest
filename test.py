from xlrd import open_workbook
import pymysql
import pymysql.cursors
import datetime

if __name__ == "__main__":
    dt = datetime.datetime.strptime("20130125", '%Y%m%d').strftime('%Y-%m-%d')
    print(dt)
    exit(1)

    #wb = load_workbook('C:/Users/blueplanet/Desktop/MovieCenter/excel範本/膠片Excel.xlsx')
    wb = open_workbook('C:/Users/blueplanet/Desktop/MovieCenter/excel範本/膠片Excel.xlsx')
    values = []
    for s in wb.sheets():
        # print('Sheet:',s.name)
        for row in range(1, s.nrows):
            col_names = s.row(0)
            # print(s.row(0))
            col_value = []
            for name, col in zip(col_names, range(s.ncols)):
                # print(s.cell(row, col).value)
                value = (s.cell(row, col).value)
                try:
                    value = str(int(value))
                except:
                    pass
                col_value.append((s.name, name.value, value))
            values.append(col_value)
    # print(values)

    # src = u"中文"
    # src = src.encode('gbk')
    # print(src)
    # src = src.decode('latin1')
    # print(src)

    conn = pymysql.connect(host='localhost', port=3306, user='admin', passwd='', db='test', charset="utf8")
    # conn.set_charset('utf8')

    cur = conn.cursor()
    # cur.execute("SELECT * FROM 膠片")
    cur.execute("insert into 膠片(藏品類型) values('QQ')")

    print(cur.description)
    print()

    for row in cur:
        print(row)

    cur.close()
    conn.commit()
    conn.close()