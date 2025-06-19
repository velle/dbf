import dbf

table = dbf.Table(filename='001.dbf')
table.open(dbf.READ_ONLY) # necessary

for record in table:
        print('----------------')
        print(record)
