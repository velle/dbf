# xBase Language vs python dbf

This document tries to explain how xBase can be used to access and manipulate
dbf files, and at the same time showing the python dbf equivalent. If you did
not know already, it will probably show how dbf is in some ways modeled after
how the original dbf tools worked, including naming of variables and methods.

## Schema manipulation

### CREATE TABLE

#### xBase command:
```
. CREATE TABLE person ( ;
    ID      N(5,0), ;
    NAME    C(20), ;
    AGE     N(3,0) ;
  )
```

#### python dbf equivalent:
```
dbf.Table(
  'person.dbf', 
  'ID N(5,0), NAME C(20), AGE N(3,0)'
)
```

### LIST STRUCTURE

#### xBase command:
```
. USE PERSON
. LIST STRUCTURE
ID       N(5,0)
NAME     C(20)
AGE      N(3,0)
```

#### python dbf equivalent:
```
table = dbf.Table(
  'person.dbf'
)
table.open(dbf.READ_ONLY)
print(table.structure()) # ['ID N(5,0)', 'NAME C(20)', 'AGE N(3,0)']
```
