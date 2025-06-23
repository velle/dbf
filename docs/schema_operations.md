# Schema operations with dbf module

This article handles making changes to the schema of a table (adding/deleting
fields, changing field types, etc) as opposed to operations on the data 
(inserting/deleting rows, updating row data, etc.).

Some operations are very easy to do with dbf, while for some, you need to
use workarounds.

### Add field

With test.db being an existing dbf file table.

    tbl = dbf.Table('test.dbf')
    tbl.open(dbf.READ_WRITE)
    tbl.add_field('nickname C(12)')
    # operation is applied to file instantly


The argument can be either Iterable or str, in the form:
    - 'nickname C(20)'
    - 'nickname C;bodyage N'
    - ['nickname C']
    - ['nickname C', 'bodyage N(3,0)']


### Drop/delete field

In the dBASE gui this was called "Deleting" a "Field". In modern database terminology it corresponds to dropping a column. 

    tbl = dbf.Table('test.dbf')
    tbl.open(dbf.READ_WRITE)
    tbl.delete_fields('name')
    # operation is applied to file instantly

The argument can be either Iterable or str, in the form:
    - 'name'
    - 'name;age'
    - ' name; age '
    - ['name']
    - ['name', 'age']


### Renaming field

```
    tbl = dbf.Table('test.dbf')
    tbl.open(dbf.READ_WRITE)
    rename(tbl, 'name', 'birthname')
    # operation is applied to file instantly
```


### Resizing field

```
    tbl = dbf.Table('test.dbf')
    tbl.open(dbf.READ_WRITE)
    resize(tbl, 'name', 'C(40)')
    # operation is applied to file instantly
```


### Change/alter field type

dbf-module does not directly support this, but this function does:

```
import dbf

def alter_type(tbl, fieldname, new_fieldspec):
    # Get original structure
    old_fields = [(f.name, f.type + f.length + (',' + str(f.decimal_count) if f.decimal_count else ''))
                  for f in tbl.structure()]
    
    # Construct new structure
    new_fields = []
    for name, spec in old_fields:
        if name.lower() == fieldname.lower():
            new_fields.append((name, new_fieldspec))
        else:
            new_fields.append((name, spec))

    # Create a temporary new table
    new_table = dbf.Table(tbl.filename + '_tmp', new_fields)
    new_table.open(mode=dbf.READ_WRITE)
    
    # Copy records
    for record in tbl:
        new_record = {}
        for field in tbl.field_names:
            if field.lower() == fieldname.lower():
                # Optional: attempt conversion
                value = record[field]
                try:
                    # Let dbf handle type coercion
                    new_record[field] = value
                except Exception:
                    new_record[field] = None  # or raise
            else:
                new_record[field] = record[field]
        new_table.append(new_record)

    tbl.close()
    new_table.close()

    # Replace original file
    dbf.delete(tbl.filename)
    dbf.rename(new_table.filename, tbl.filename)
```

Usage:

```
    tbl = dbf.Table('test.dbf')
    tbl.open(dbf.READ_WRITE)
    rename(tbl, 'name', 'birthname')
    # operation is applied to file instantly
```


### Reorder fields

Tables do have a fixed field order, and for some applications it matters.

dbf-module does not directly support this, but this function does:

```
import dbf
import os

def reorder(tbl, field_name_list):
    # Ensure table is open
    if not tbl.opened:
        tbl.open(dbf.READ_ONLY)
    
    # Get current structure
    old_structure = {f.name.lower(): f for f in tbl.structure()}
    
    # Normalize and validate input
    new_order = [f.lower() for f in field_name_list]
    if set(new_order) != set(old_structure.keys()):
        raise ValueError("Field names do not match current table structure.")
    
    # Create new field structure in new order
    new_fields = []
    for fname in new_order:
        f = old_structure[fname]
        spec = f.type + f.length
        if f.decimal_count:
            spec += ',' + str(f.decimal_count)
        new_fields.append((f.name, spec))

    # Create a new table with reordered fields
    tmp_filename = tbl.filename + '_reordered'
    new_tbl = dbf.Table(tmp_filename, new_fields)
    new_tbl.open(mode=dbf.READ_WRITE)

    # Copy data into new table with reordered fields
    for rec in tbl:
        new_rec = {f.name: rec[f.name] for f in new_tbl.structure()}
        new_tbl.append(new_rec)

    # Close and replace the original table
    tbl.close()
    new_tbl.close()
    os.remove(tbl.filename)
    os.rename(tmp_filename, tbl.filename)
```


## foo

./tables.py:    def resize_field(self, chosen, new_size):
