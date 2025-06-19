import dbf

table = dbf.Table(
        filename='001.dbf',
        field_specs='name C(25); age N(3,0); birth D; qualified L',
        )

table.open(dbf.READ_WRITE)

for datum in (
        ('Spanky', 7, dbf.Date.fromymd('20010315'), False),
        ('Spunky', 23, dbf.Date(1989, 7, 23), True),
        ('Sparky', 99, dbf.Date(), dbf.Unknown),
        ):
    table.append(datum)
