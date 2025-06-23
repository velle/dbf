import os
import tempfile
import datetime

import dbf
from dbf import *
from dbf.constants import *

from common import *


class TestDbfFunctions(TestCase):

    def setUp(self):
        "create a dbf and vfp table"
        self.empty_dbf_table = Table(
            os.path.join(tempdir, 'emptytemptable'),
            'name C(25); paid L; qty N(11,5); orderdate D; desc M', dbf_type='db3'
            )
        self.dbf_table = table = Table(
            os.path.join(tempdir, 'temptable'),
            'name C(25); paid L; qty N(11,5); orderdate D; desc M', dbf_type='db3'
            )
        table.open(mode=READ_WRITE)
        namelist = self.dbf_namelist = []
        paidlist = self.dbf_paidlist = []
        qtylist = self.dbf_qtylist = []
        orderlist = self.dbf_orderlist = []
        desclist = self.dbf_desclist = []
        for i in range(len(floats)):
            name = '%-25s' % words[i]
            paid = len(words[i]) % 3 == 0
            qty = floats[i]
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            namelist.append(name)
            paidlist.append(paid)
            qtylist.append(qty)
            orderlist.append(orderdate)
            desclist.append(desc)
            table.append({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc})
        table.close()

        self.empty_vfp_table = Table(
                os.path.join(tempdir, 'emptytempvfp'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;'
                ' weight F(18,3); age I; meeting T; misc G; photo P; price Y;'
                ' dist B BINARY; atom I BINARY; wealth Y BINARY;'
                ,
                dbf_type='vfp',
                )
        self.odd_memo_vfp_table = Table(
                os.path.join(tempdir, 'emptytempvfp'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;'
                ' weight F(18,3); age I; meeting T; misc G; photo P; price Y;'
                ' dist B BINARY; atom I BINARY; wealth Y BINARY;'
                ,
                dbf_type='vfp',
                memo_size=48,
                )
        self.vfp_table = table = Table(
                os.path.join(tempdir, 'tempvfp'),
                'name C(25); paid L; qty N(11,5); orderdate D; desc M; mass B;'
                ' weight F(18,3); age I; meeting T; misc G; photo P; price Y;'
                ' dist B BINARY; atom I BINARY; wealth Y BINARY;'
                ,
                dbf_type='vfp',
                )
        table.open(mode=READ_WRITE)
        namelist = self.vfp_namelist = []
        paidlist = self.vfp_paidlist = []
        qtylist = self.vfp_qtylist = []
        orderlist = self.vfp_orderlist = []
        desclist = self.vfp_desclist = []
        masslist = self.vfp_masslist = []
        weightlist = self.vfp_weightlist = []
        agelist = self.vfp_agelist = []
        meetlist = self.vfp_meetlist = []
        misclist = self.vfp_misclist = []
        photolist = self.vfp_photolist = []
        pricelist = self.vfp_pricelist = []
        for i in range(len(floats)):
            name = words[i]
            paid = len(words[i]) % 3 == 0
            qty = floats[i]
            price = Decimal(round(floats[i] * 2.182737, 4))
            orderdate = datetime.date((numbers[i] + 1) * 2, (numbers[i] % 12) +1, (numbers[i] % 27) + 1)
            desc = ' '.join(words[i:i+50])
            mass = floats[i] * floats[i] / 2.0
            weight = round(floats[i] * 3, 3)
            age = numbers[i]
            meeting = datetime.datetime((numbers[i] + 2000), (numbers[i] % 12)+1, (numbers[i] % 28)+1, \
                      (numbers[i] % 24), numbers[i] % 60, (numbers[i] * 3) % 60)
            misc = ' '.join(words[i:i+50:3]).encode('latin1')
            photo = ' '.join(words[i:i+50:7]).encode('latin1')
            namelist.append('%-25s' % name)
            paidlist.append(paid)
            qtylist.append(qty)
            pricelist.append(price)
            orderlist.append(orderdate)
            desclist.append(desc)
            masslist.append(mass)
            weightlist.append(weight)
            agelist.append(age)
            meetlist.append(meeting)
            misclist.append(misc)
            photolist.append(photo)
            meeting = datetime.datetime((numbers[i] + 2000), (numbers[i] % 12)+1, (numbers[i] % 28)+1,
                      (numbers[i] % 24), numbers[i] % 60, (numbers[i] * 3) % 60)
            table.append({'name':name, 'paid':paid, 'qty':qty, 'orderdate':orderdate, 'desc':desc,
                    'mass':mass, 'weight':weight, 'age':age, 'meeting':meeting, 'misc':misc, 'photo':photo,
                    'price':price, 'dist':mass, 'atom':age, 'wealth':price})
        table.close()

    def tearDown(self):
        self.dbf_table.close()
        self.vfp_table.close()

    def test_add_fields_to_dbf_table(self):
        "dbf table:  adding and deleting fields"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        dbf._debug = True
        namelist = self.dbf_namelist
        paidlist = self.dbf_paidlist
        qtylist = self.dbf_qtylist
        orderlist = self.dbf_orderlist
        desclist = self.dbf_desclist
        table.delete_fields('name')
        table.close()
        table = Table(table.filename, dbf_type='db3')
        table.open(mode=READ_WRITE)
        for field in table.field_names:
            self.assertEqual(1, table.field_names.count(field))
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].paid, paidlist[i])
            self.assertEqual(record.paid, paidlist[i])
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(table[i].desc, desclist[i])
            self.assertEqual(record.desc, desclist[i])
            i += 1
        first, middle, last = table[0], table[len(table)//2], table[-1]
        table.delete_fields('paid, orderdate')
        for field in table.field_names:
            self.assertEqual(1, table.field_names.count(field))
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].desc, desclist[i])
            self.assertEqual(record.desc, desclist[i])
            i += 1
        self.assertEqual(i, len(table))
        self.assertTrue('paid' not in dbf.field_names(first))
        self.assertTrue('orderdate' not in dbf.field_names(middle))
        self.assertTrue('name' not in dbf.field_names(last))
        table.add_fields('name C(25); paid L; orderdate D')
        for field in table.field_names:
            self.assertEqual(1, table.field_names.count(field))
        self.assertEqual(i, len(table))
        i = 0
        for i, record in enumerate(table):
            self.assertEqual(record.name, ' ' * 25)
            self.assertEqual(record.paid, None)
            self.assertEqual(record.orderdate, None)
            self.assertEqual(record.desc, desclist[i])
            i += 1
        self.assertEqual(i, len(table))
        i = 0
        for record in table:
            data = dict()
            data['name'] = namelist[dbf.recno(record)]
            data['paid'] = paidlist[dbf.recno(record)]
            data['orderdate'] = orderlist[dbf.recno(record)]
            dbf.gather(record, data)
            i += 1
        self.assertEqual(i, len(table))
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].name, namelist[i])
            self.assertEqual(record.name, namelist[i])
            self.assertEqual(table[i].paid, paidlist[i])
            self.assertEqual(record.paid, paidlist[i])
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(table[i].desc, desclist[i])
            self.assertEqual(record.desc, desclist[i])
            i += 1
        table.close()

    def test_add_fields_to_vfp_table(self):
        "vfp table:  adding and deleting fields"
        table = self.vfp_table
        table.open(mode=READ_WRITE)
        namelist = self.vfp_namelist
        paidlist = self.vfp_paidlist
        qtylist = self.vfp_qtylist
        orderlist = self.vfp_orderlist
        desclist = self.vfp_desclist
        masslist = self.vfp_masslist
        weightlist = self.vfp_weightlist
        agelist = self.vfp_agelist
        meetlist = self.vfp_meetlist
        misclist = self.vfp_misclist
        photolist = self.vfp_photolist
        pricelist = self.vfp_pricelist
        self.assertEqual(len(table), len(floats))
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].name, namelist[i])
            self.assertEqual(record.name, namelist[i])
            self.assertEqual(table[i].paid, paidlist[i])
            self.assertEqual(record.paid, paidlist[i])
            self.assertTrue(abs(table[i].qty - qtylist[i]) < .00001)
            self.assertTrue(abs(record.qty - qtylist[i]) < .00001)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(table[i].desc, desclist[i])
            self.assertEqual(record.desc, desclist[i])
            self.assertEqual(record.mass, masslist[i])
            self.assertEqual(table[i].mass, masslist[i])
            self.assertEqual(record.dist, masslist[i])
            self.assertEqual(table[i].dist, masslist[i])
            self.assertEqual(record.weight, weightlist[i])
            self.assertEqual(table[i].weight, weightlist[i])
            self.assertEqual(record.age, agelist[i])
            self.assertEqual(table[i].age, agelist[i])
            self.assertEqual(record.atom, agelist[i])
            self.assertEqual(table[i].atom, agelist[i])
            self.assertEqual(record.meeting, meetlist[i])
            self.assertEqual(table[i].meeting, meetlist[i])
            self.assertEqual(record.misc, misclist[i])
            self.assertEqual(table[i].misc, misclist[i])
            self.assertEqual(record.photo, photolist[i])
            self.assertEqual(table[i].photo, photolist[i])
            self.assertEqual(round(record.price, 4), round(pricelist[i], 4))
            self.assertEqual(round(table[i].price, 4), round(pricelist[i], 4))
            self.assertTrue(round(record.wealth, 4), round(pricelist[i], 4))
            self.assertTrue(round(table[i].wealth, 4), round(pricelist[i], 4))
            i += 1
        table.delete_fields('desc')
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].name, namelist[i])
            self.assertEqual(record.name, namelist[i])
            self.assertEqual(table[i].paid, paidlist[i])
            self.assertEqual(record.paid, paidlist[i])
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(record.weight, weightlist[i])
            self.assertEqual(table[i].weight, weightlist[i])
            self.assertEqual(record.age, agelist[i])
            self.assertEqual(table[i].age, agelist[i])
            self.assertEqual(record.atom, agelist[i])
            self.assertEqual(table[i].atom, agelist[i])
            self.assertEqual(record.meeting, meetlist[i])
            self.assertEqual(table[i].meeting, meetlist[i])
            self.assertEqual(record.misc, misclist[i])
            self.assertEqual(table[i].misc, misclist[i])
            self.assertEqual(record.photo, photolist[i])
            self.assertEqual(table[i].photo, photolist[i])
            self.assertEqual(record.mass, masslist[i])
            self.assertEqual(table[i].mass, masslist[i])
            self.assertEqual(record.dist, masslist[i])
            self.assertEqual(table[i].dist, masslist[i])
            self.assertEqual(round(record.price, 4), round(pricelist[i], 4))
            self.assertEqual(round(table[i].price, 4), round(pricelist[i], 4))
            self.assertTrue(round(record.wealth, 4), round(pricelist[i], 4))
            self.assertTrue(round(table[i].wealth, 4), round(pricelist[i], 4))
            i += 1
        table.delete_fields('paid, mass')
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].name, namelist[i])
            self.assertEqual(record.name, namelist[i])
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(record.weight, weightlist[i])
            self.assertEqual(table[i].weight, weightlist[i])
            self.assertEqual(record.age, agelist[i])
            self.assertEqual(table[i].age, agelist[i])
            self.assertEqual(record.atom, agelist[i])
            self.assertEqual(table[i].atom, agelist[i])
            self.assertEqual(record.meeting, meetlist[i])
            self.assertEqual(table[i].meeting, meetlist[i])
            self.assertEqual(record.misc, misclist[i])
            self.assertEqual(table[i].misc, misclist[i])
            self.assertEqual(record.photo, photolist[i])
            self.assertEqual(table[i].photo, photolist[i])
            self.assertEqual(record.dist, masslist[i])
            self.assertEqual(table[i].dist, masslist[i])
            self.assertEqual(round(record.price, 4), round(pricelist[i], 4))
            self.assertEqual(round(table[i].price, 4), round(pricelist[i], 4))
            self.assertTrue(round(record.wealth, 4), round(pricelist[i], 4))
            self.assertTrue(round(table[i].wealth, 4), round(pricelist[i], 4))
            i += 1
        table.add_fields('desc M; paid L; mass B')
        i = 0
        for record in table:
            self.assertEqual(record.desc, unicode(''))
            self.assertEqual(record.paid is None, True)
            self.assertEqual(record.mass, 0.0)
            i += 1
        self.assertEqual(i, len(table))
        i = 0
        for record in Process(table):
            record.desc = desclist[dbf.recno(record)]
            record.paid = paidlist[dbf.recno(record)]
            record.mass = masslist[dbf.recno(record)]
            i += 1
        self.assertEqual(i, len(table))
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            self.assertEqual(table[i].name, namelist[i])
            self.assertEqual(record.name, namelist[i])
            self.assertEqual(table[i].paid, paidlist[i])
            self.assertEqual(record.paid, paidlist[i])
            self.assertEqual(abs(table[i].qty - qtylist[i]) < .00001, True)
            self.assertEqual(abs(record.qty - qtylist[i]) < .00001, True)
            self.assertEqual(table[i].orderdate, orderlist[i])
            self.assertEqual(record.orderdate, orderlist[i])
            self.assertEqual(table[i].desc, desclist[i])
            self.assertEqual(record.desc, desclist[i])
            self.assertEqual(record.mass, masslist[i])
            self.assertEqual(table[i].mass, masslist[i])
            self.assertEqual(record.dist, masslist[i])
            self.assertEqual(table[i].dist, masslist[i])
            self.assertEqual(record.weight, weightlist[i])
            self.assertEqual(table[i].weight, weightlist[i])
            self.assertEqual(record.age, agelist[i])
            self.assertEqual(table[i].age, agelist[i])
            self.assertEqual(record.atom, agelist[i])
            self.assertEqual(table[i].atom, agelist[i])
            self.assertEqual(record.meeting, meetlist[i])
            self.assertEqual(table[i].meeting, meetlist[i])
            self.assertEqual(record.misc, misclist[i])
            self.assertEqual(table[i].misc, misclist[i])
            self.assertEqual(record.photo, photolist[i])
            self.assertEqual(table[i].photo, photolist[i])
            self.assertEqual(round(record.price, 4), round(pricelist[i], 4))
            self.assertEqual(round(table[i].price, 4), round(pricelist[i], 4))
            self.assertTrue(round(record.wealth, 4), round(pricelist[i], 4))
            self.assertTrue(round(table[i].wealth, 4), round(pricelist[i], 4))
            i += 1
        table.close()

    def test_len_contains_iter(self):
        "basic function tests - len, contains & iterators"
        table = self.dbf_table.open()
        for field in table.field_names:
            self.assertEqual(1, table.field_names.count(field))
        length = sum([1 for rec in table])
        self.assertEqual(length, len(table))
        i = 0
        for record in table:
            self.assertEqual(record, table[i])
            self.assertTrue(record in table)
            self.assertTrue(tuple(record) in table)
            self.assertTrue(scatter(record) in table)
            self.assertTrue(create_template(record) in table)
            i += 1
        self.assertEqual(i, len(table))
        table.close()

    def test_undelete(self):
        "delete, undelete"
        table = Table(':memory:', 'name C(10)', dbf_type='db3', on_disk=False)
        table.open(mode=READ_WRITE)
        table.append()
        self.assertEqual(table.next_record, table[0])
        table = Table(':memory:', 'name C(10)', dbf_type='db3', on_disk=False)
        table.open(mode=READ_WRITE)
        table.append(multiple=10)
        self.assertEqual(table.next_record, table[0])
        table = self.dbf_table              # Table(os.path.join(tempdir, 'temptable'), dbf_type='db3')
        table.open(mode=READ_WRITE)
        total = len(table)
        table.bottom()
        self.assertEqual(dbf.recno(table.current_record), total)
        table.top()
        self.assertEqual(dbf.recno(table.current_record), -1)
        table.goto(27)
        self.assertEqual(dbf.recno(table.current_record), 27)
        table.goto(total-1)
        self.assertEqual(dbf.recno(table.current_record), total-1)
        table.goto(0)
        self.assertEqual(dbf.recno(table.current_record), 0)
        self.assertRaises(IndexError, table.goto, total)
        self.assertRaises(IndexError, table.goto, -len(table)-1)
        table.top()
        self.assertRaises(dbf.Bof, table.skip, -1)
        table.bottom()
        self.assertRaises(Eof, table.skip)
        for record in table:
            dbf.delete(record)
        active_records = table.create_index(active)
        active_records.top()
        self.assertRaises(Eof, active_records.skip)
        dbf._debug = True
        active_records.bottom()
        self.assertRaises(Bof, active_records.skip, -1)
        for record in table:
            dbf.undelete(record)

        # delete every third record
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            if i % 3 == 0:
                dbf.delete(record)
            i += 1
        i = 0
        # and verify
        for record in table:
            self.assertEqual(dbf.is_deleted(record), i%3==0)
            self.assertEqual(dbf.is_deleted(table[i]), i%3==0)
            i += 1

        # check that deletes were saved to disk..
        table.close()
        table = Table(os.path.join(tempdir, 'temptable'), dbf_type='db3')
        table.open(mode=READ_WRITE)
        active_records = table.create_index(active)
        i = 0
        for record in table:
            self.assertEqual(dbf.is_deleted(record), i%3==0)
            self.assertEqual(dbf.is_deleted(table[i]), i%3==0)
            i += 1

        # verify record numbers
        i = 0
        for record in table:
            self.assertEqual(dbf.recno(record), i)
            i += 1

        # verify that deleted records are skipped
        i = 0
        for record in active_records:
            self.assertNotEqual(dbf.recno(record)%3, 0)
        active_records.goto(1)
        active_records.skip()
        self.assertEqual(dbf.recno(active_records.current_record), 4)
        active_records.skip(-1)
        self.assertEqual(dbf.recno(active_records.current_record), 2)

        # verify that deleted records are skipped in slices
        list_of_records = active_records[3:6]
        self.assertEqual(len(list_of_records), 3)
        self.assertEqual(dbf.recno(list_of_records[0]), 5)
        self.assertEqual(dbf.recno(list_of_records[1]), 7)
        self.assertEqual(dbf.recno(list_of_records[2]), 8)

        # verify behavior when all records are deleted
        for record in table:
            dbf.delete(record)
        active_records.bottom()
        self.assertRaises(Eof, active_records.skip)
        self.assertEqual(active_records.eof, True)
        active_records.top()
        self.assertRaises(Bof, active_records.skip, -1)
        self.assertEqual(active_records.bof, True)

        # verify deleted records are seen with active record index
        deleted_records = table.create_index(inactive)
        i = 0
        for record in deleted_records:
            self.assertEqual(dbf.recno(record), i)
            i += 1

        # verify undelete using table[index]
        for record in table:
            dbf.delete(record)
            self.assertTrue(dbf.is_deleted(record))
        for i, record in enumerate(table):
            dbf.undelete(table[i])
            self.assertEqual(dbf.is_deleted(record), False)
            self.assertEqual(dbf.is_deleted(table[i]), False)
            self.assertFalse(record in deleted_records)

        # verify all records have been undeleted (recalled)
        self.assertEqual(len(active_records), len(table))
        self.assertEqual(len(deleted_records), 0)
        table.close()

    def test_finding_ordering_searching(self):
        "finding, ordering, searching"
        table = self.dbf_table
        table.open(mode=READ_WRITE)

        # find (brute force)
        unordered = []
        for record in table:
            unordered.append(record.name)
        for word in unordered:                                  # returns records
            # records = table.query("select * where name == %r" % word)
            # self.assertEqual(len(records), unordered.count(word))
            records = [rec for rec in table if rec.name == word]
            self.assertEqual(len(records), unordered.count(word))

        # ordering by one field
        ordered = unordered[:]
        ordered.sort()
        name_index = table.create_index(lambda rec: rec.name)
        self.assertEqual(list(name_index[::-1]), list(reversed(name_index)))
        i = 0
        for record in name_index:
            self.assertEqual(record.name, ordered[i])
            i += 1

        # search (BINARY)
        for word in unordered:
            records = name_index.search(match=word)
            self.assertEqual(len(records), unordered.count(word), "num records: %d\nnum words: %d\nfailure with %r" % (len(records), unordered.count(word), word))
            records = table.query("select * where name == %r" % word)
            self.assertEqual(len(records), unordered.count(word))
            records = dbf.pqlc(table, "select * where name == %r" % word)
            self.assertEqual(len(records), unordered.count(word))

        # ordering by two fields
        ordered = unordered[:]
        ordered.sort()
        nd_index = table.create_index(lambda rec: (rec.name, rec.desc))
        self.assertEqual(list(nd_index[::-1]), list(reversed(nd_index)))
        i = 0
        for record in nd_index:
            self.assertEqual(record.name, ordered[i])
            i += 1

        # search (BINARY)
        for word in unordered:
            records = nd_index.search(match=(word, ), partial=True)
            ucount = sum([1 for wrd in unordered if wrd.startswith(word)])
            self.assertEqual(len(records), ucount)

        # partial search
        rec = nd_index[7]
        self.assertTrue(nd_index.search((rec.name, rec.desc[:4]), partial=True))

        for record in table[::2]:
            dbf.write(record, qty=-record.qty)
        unordered = []
        for record in table:
            unordered.append(record.qty)
        ordered = unordered[:]
        ordered.sort()
        qty_index = table.create_index(lambda rec: rec.qty)
        self.assertEqual(list(qty_index[::-1]), list(reversed(qty_index)))
        i = 0
        for record in qty_index:
            self.assertEqual(record.qty, ordered[i])
            i += 1
        for number in unordered:
            records = qty_index.search(match=(number, ))
            self.assertEqual(len(records), unordered.count(number))

        table.close()

    def test_scatter_gather_new(self):
        "scattering and gathering fields, and new()"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        table2 = table.new(os.path.join(tempdir, 'temptable2'))
        table2.open(mode=READ_WRITE)
        for record in table:
            table2.append()
            newrecord = table2[-1]
            testdict = dbf.scatter(record)
            for key in field_names(testdict):
                self.assertEqual(testdict[key], record[key])
            dbf.gather(newrecord, dbf.scatter(record))
            for field in dbf.field_names(record):
                self.assertEqual(newrecord[field], record[field])
        table2.close()
        table2 = None
        table2 = Table(os.path.join(tempdir, 'temptable2'), dbf_type='db3')
        table2.open(mode=READ_WRITE)
        for i in range(len(table)):
            temp1 = dbf.scatter(table[i])
            temp2 = dbf.scatter(table2[i])
            for key in field_names(temp1):
                self.assertEqual(temp1[key], temp2[key])
            for key in field_names(temp2):
                self.assertEqual(temp1[key], temp2[key])
        table2.close()
        table3 = table.new(':memory:', on_disk=False)
        table3.open(mode=READ_WRITE)
        for record in table:
            table3.append(record)
        table4 = self.vfp_table
        table4.open(mode=READ_WRITE)
        table5 = table4.new(':memory:', on_disk=False)
        table5.open(mode=READ_WRITE)
        for record in table4:
            table5.append(record)
        table.close()
        table3.close()
        table4.close()
        table5.close()

    def test_rename_contains_has_key(self):
        "renaming fields, __contains__, has_key"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        for field in table.field_names:
            oldfield = field
            table.rename_field(oldfield, 'newfield')
            self.assertEqual(oldfield in table.field_names, False)
            self.assertEqual('newfield' in table.field_names, True)
            table.close()
            table = Table(os.path.join(tempdir, 'temptable'), dbf_type='db3')
            table.open(mode=READ_WRITE)
            self.assertEqual(oldfield in table.field_names, False)
            self.assertEqual('newfield' in table.field_names, True)
            table.rename_field('newfield', oldfield)
            self.assertEqual(oldfield in table.field_names, True)
            self.assertEqual('newfield' in table.field_names, False)
        table.close()

    def test_dbf_record_kamikaze(self):
        "kamikaze"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        table2 = table.new(os.path.join(tempdir, 'temptable2'))
        table2.open(mode=READ_WRITE)
        for record in table:
            table2.append(record)
            newrecord = table2[-1]
            for key in table.field_names:
                if key not in table.memo_types:
                    self.assertEqual(newrecord[key], record[key])
            for field in dbf.field_names(newrecord):
                if key not in table2.memo_types:
                    self.assertEqual(newrecord[field], record[field])
        table2.close()
        table2 = Table(os.path.join(tempdir, 'temptable2'), dbf_type='db3')
        table2.open(mode=READ_WRITE)
        for i in range(len(table)):
            dict1 = dbf.scatter(table[i], as_type=dict)
            dict2 = dbf.scatter(table2[i], as_type=dict)
            for key in dict1.keys():
                if key not in table.memo_types:
                    self.assertEqual(dict1[key], dict2[key])
            for key in dict2.keys():
                if key not in table2.memo_types:
                    self.assertEqual(dict1[key], dict2[key])
        for i in range(len(table)):
            template1 = dbf.scatter(table[i])
            template2 = dbf.scatter(table2[i])
            for key in dbf.field_names(template1):
                if key not in table.memo_types:
                    self.assertEqual(template1[key], template2[key])
            for key in dbf.field_names(template2):
                if key not in table2.memo_types:
                    self.assertEqual(template1[key], template2[key])
        table.close()
        table2.close()

    def test_multiple_append(self):
        "multiple append"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        table2 = table.new(os.path.join(tempdir, 'temptable2'))
        table2.open(mode=READ_WRITE)
        record = table.next_record
        table2.append(dbf.scatter(record), multiple=100)
        for samerecord in table2:
            for field in dbf.field_names(record):
                self.assertEqual(record[field], samerecord[field])
        table2.close()
        table2 = Table(os.path.join(tempdir, 'temptable2'), dbf_type='db3')
        table2.open(mode=READ_WRITE)
        for samerecord in table2:
            for field in dbf.field_names(record):
                self.assertEqual(record[field], samerecord[field])
        table2.close()
        table3 = table.new(os.path.join(tempdir, 'temptable3'))
        table3.open(mode=READ_WRITE)
        record = table.next_record
        table3.append(record, multiple=100)
        for samerecord in table3:
            for field in dbf.field_names(record):
                self.assertEqual(record[field], samerecord[field])
        table3.close()
        table3 = Table(os.path.join(tempdir, 'temptable3'), dbf_type='db3')
        table3.open(mode=READ_WRITE)
        for samerecord in table3:
            for field in dbf.field_names(record):
                self.assertEqual(record[field], samerecord[field])
        table3.close()
        table.close()

    def test_slices(self):
        "slices"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        slice1 = [table[0], table[1], table[2]]
        self.assertEqual(slice1, list(table[:3]))
        slice2 = [table[-3], table[-2], table[-1]]
        self.assertEqual(slice2, list(table[-3:]))
        slice3 = [record for record in table]
        self.assertEqual(slice3, list(table[:]))
        slice4 = [table[9]]
        self.assertEqual(slice4, list(table[9:10]))
        slice5 = [table[15], table[16], table[17], table[18]]
        self.assertEqual(slice5, list(table[15:19]))
        slice6 = [table[0], table[2], table[4], table[6], table[8]]
        self.assertEqual(slice6, list(table[:9:2]))
        slice7 = [table[-1], table[-2], table[-3]]
        self.assertEqual(slice7, list(table[-1:-4:-1]))
        table.close()

    def test_record_reset(self):
        "reset record"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        for record in table:
            with record:
                self.assertTrue(record.qty)
                dbf.reset(record, keep_fields=['name'])
            self.assertFalse(record.qty)
            self.assertTrue(record.name)
        for record in table:
            dbf.reset(record)
        self.assertEqual(table[0].name, table[1].name)
        dbf.write(table[0], name='Python rocks!')
        self.assertNotEqual(table[0].name, table[1].name)
        table.close()

    def test_adding_memos(self):
        "adding memos to existing records"
        table = Table(':memory:', 'name C(50); age N(3,0)', dbf_type='db3', on_disk=False)
        table.open(mode=READ_WRITE)
        table.append(('user', 0))
        table.add_fields('motto M')
        dbf.write(table[0], motto='Are we there yet??')
        self.assertEqual(table[0].motto, 'Are we there yet??')
        table.close()
        table = Table(os.path.join(tempdir, 'temptable4'), 'name C(50); age N(3,0)', dbf_type='db3')
        table.open(mode=READ_WRITE)
        table.append(('user', 0))
        table.close()
        table.open(mode=READ_WRITE)
        table.close()
        table = Table(os.path.join(tempdir, 'temptable4'), dbf_type='db3')
        table.open(mode=READ_WRITE)
        table.add_fields('motto M')
        dbf.write(table[0], motto='Are we there yet??')
        self.assertEqual(table[0].motto, 'Are we there yet??')
        table.close()
        table = Table(os.path.join(tempdir, 'temptable4'), dbf_type='db3')
        table.open(mode=READ_WRITE)
        self.assertEqual(table[0].motto, 'Are we there yet??')
        table.close()
        table = Table(os.path.join(tempdir, 'temptable4'), 'name C(50); age N(3,0)', dbf_type='vfp')
        table.open(mode=READ_WRITE)
        table.append(('user', 0))
        table.close()
        table.open(mode=READ_WRITE)
        table.close()
        table = Table(os.path.join(tempdir, 'temptable4'), dbf_type='vfp')
        table.open(mode=READ_WRITE)
        table.add_fields('motto M')
        dbf.write(table[0], motto='Are we there yet??')
        self.assertEqual(table[0].motto, 'Are we there yet??')
        table.close()
        table = Table(os.path.join(tempdir, 'temptable4'), dbf_type='vfp')
        table.open(mode=READ_WRITE)
        self.assertEqual(table[0].motto, 'Are we there yet??')
        table.close()

    def test_from_csv(self):
        "from_csv"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        dbf.export(table, table.filename, header=False)
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'))
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]), csvtable[i][j])
        csvtable.close()
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'), to_disk=True, filename=os.path.join(tempdir, 'temptable5'))
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]).strip(), csvtable[i][j].strip())
        csvtable.close()
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'), field_names=['field1','field2'])
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]), csvtable[i][j])
        csvtable.close()
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'), field_names=['field1','field2'], to_disk=True, filename=os.path.join(tempdir, 'temptable5'))
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]).strip(), csvtable[i][j].strip())
        csvtable.close()
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'), extra_fields=['count N(5,0)','id C(10)'])
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]), csvtable[i][j])
        csvtable.close()
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'), extra_fields=['count N(5,0)','id C(10)'], to_disk=True, filename=os.path.join(tempdir, 'temptable5'))
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]).strip(), csvtable[i][j].strip())
        csvtable.close()
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'), field_names=['name','qty','paid','desc'], extra_fields='test1 C(15);test2 L'.split(';'))
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]), csvtable[i][j])
        csvtable.close()
        csvtable = dbf.from_csv(os.path.join(tempdir, 'temptable.csv'), field_names=['name','qty','paid','desc'], extra_fields='test1 C(15);test2 L'.split(';'), to_disk=True, filename=os.path.join(tempdir, 'temptable5'))
        csvtable.open(mode=READ_WRITE)
        for i in index(table):
            for j in index(table.field_names):
                self.assertEqual(str(table[i][j]).strip(), csvtable[i][j].strip())
        csvtable.close()

    def test_resize_empty(self):
        "resize"
        table = self.empty_dbf_table
        table.open(mode=READ_WRITE)
        table.resize_field('name', 40)
        table.close()

    def test_resize(self):
        "resize"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        test_record = dbf.scatter(table[5])
        test_record = dbf.scatter(table[5])
        table.resize_field('name', 40)
        new_record = dbf.scatter(table[5])
        self.assertEqual(test_record['orderdate'], new_record['orderdate'])
        table.close()

    def test_memos_after_close(self):
        "memos available after close/open"
        table = dbf.Table('tempy', 'name C(20); desc M', dbf_type='db3', default_data_types=dict(C=Char))
        table.open(mode=READ_WRITE)
        table.append(('Author','dashing, debonair, delightful'))
        table.close()
        table.open(mode=READ_WRITE)
        self.assertEqual(tuple(table[0]), ('Author','dashing, debonair, delightful'))
        table.close()
        table2 = dbf.Table('tempy', 'name C(20); desc M', dbf_type='db3')
        table2.open(mode=READ_WRITE)
        table2.append(('Benedict', 'brilliant, bombastic, bothered'))
        table2.close()
        table.open(mode=READ_WRITE)
        self.assertEqual(table[0].name, 'Benedict')
        self.assertEqual(table[0].desc, 'brilliant, bombastic, bothered')
        table.close()

    def test_field_type(self):
        "table.type(field) == ('C', Char)"
        table = dbf.Table('tempy', 'name C(20); desc M', dbf_type='db3', default_data_types=dict(C=Char))
        table.open(mode=READ_WRITE)
        field_info = table.field_info('name')
        self.assertEqual(field_info, (FieldType.CHAR, 20, 0, Char))
        self.assertEqual(field_info.field_type, FieldType.CHAR)
        self.assertEqual(field_info.length, 20)
        self.assertEqual(field_info.decimal, 0)
        self.assertEqual(field_info.py_type, Char)
        table.close()

    def test_memo_after_backup(self):
        "memo fields accessible after .backup()"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        table.create_backup()
        backup = dbf.Table(table.backup)
        backup.open(mode=READ_WRITE)
        desclist = self.dbf_desclist
        for i in range(len(desclist)):
            self.assertEqual(desclist[i], backup[i].desc)
        backup.close()
        table.close()

    def test_memo_file_size_before_backup(self):
        table = self.odd_memo_vfp_table
        self.assertEqual(48, table._meta.memo_size)

    def test_memo_file_size_after_backup(self):
        table = self.odd_memo_vfp_table
        table.open(mode=READ_ONLY)
        table.create_backup()
        table.close()
        backup = dbf.Table(table.backup)
        self.assertEqual(backup._meta.memo_size, table._meta.memo_size)

    def test_write_loop(self):
        "Process loop commits changes"
        table = self.dbf_table
        table.open(mode=READ_WRITE)
        for record in Process(table):
            record.name = '!BRAND NEW NAME!'
        for record in table:
            self.assertEqual(record.name, '!BRAND NEW NAME!         ')
        table.close()

    def test_export_headers(self):
        for table in self.dbf_table, self.vfp_table:
            table.open(mode=READ_WRITE)
            dest = os.path.join(tempdir, 'test_export.csv')
            dbf.export(table, filename=dest)
            with open(dest) as fh:
                headers = fh.readline()
            self.assertEqual(headers.strip(), ','.join(table.field_names))

    def test_index_search(self):
        table = Table("unordered", "icao C(20)", default_data_types=dict(C=Char), on_disk=False).open(mode=READ_WRITE)
        icao = ("kilo charlie echo golf papa hotel delta tango india sierra juliet lima zulu mike "
                "bravo november alpha oscar quebec romeo uniform victor whiskey x-ray yankee foxtrot".split())
        for alpha in icao:
            table.append((alpha,))
        sorted = table.create_index(lambda rec: rec.icao)
        self.assertTrue(sorted.index_search('alpha'))
        self.assertTrue(sorted.index_search('bravo'))
        self.assertTrue(sorted.index_search('charlie'))
        self.assertTrue(sorted.index_search('delta'))
        self.assertTrue(sorted.index_search('echo'))
        self.assertTrue(sorted.index_search('foxtrot'))
        self.assertTrue(sorted.index_search('golf'))
        self.assertTrue(sorted.index_search('hotel'))
        self.assertTrue(sorted.index_search('india'))
        self.assertTrue(sorted.index_search('juliet'))
        self.assertTrue(sorted.index_search('kilo'))
        self.assertTrue(sorted.index_search('lima'))
        self.assertTrue(sorted.index_search('mike'))
        self.assertTrue(sorted.index_search('november'))
        self.assertTrue(sorted.index_search('oscar'))
        self.assertTrue(sorted.index_search('papa'))
        self.assertTrue(sorted.index_search('quebec'))
        self.assertTrue(sorted.index_search('romeo'))
        self.assertTrue(sorted.index_search('sierra'))
        self.assertTrue(sorted.index_search('tango'))
        self.assertTrue(sorted.index_search('uniform'))
        self.assertTrue(sorted.index_search('victor'))
        self.assertTrue(sorted.index_search('whiskey'))
        self.assertTrue(sorted.index_search('x-ray'))
        self.assertTrue(sorted.index_search('yankee'))
        self.assertTrue(sorted.index_search('zulu'))
        self.assertEqual(sorted.index_search('alpha'), 0)
        self.assertEqual(sorted.index_search('bravo'), 1)
        self.assertEqual(sorted.index_search('charlie'), 2)
        self.assertEqual(sorted.index_search('delta'), 3)
        self.assertEqual(sorted.index_search('echo'), 4)
        self.assertEqual(sorted.index_search('foxtrot'), 5)
        self.assertEqual(sorted.index_search('golf'), 6)
        self.assertEqual(sorted.index_search('hotel'), 7)
        self.assertEqual(sorted.index_search('india'), 8)
        self.assertEqual(sorted.index_search('juliet'), 9)
        self.assertEqual(sorted.index_search('kilo'), 10)
        self.assertEqual(sorted.index_search('lima'), 11)
        self.assertEqual(sorted.index_search('mike'), 12)
        self.assertEqual(sorted.index_search('november'), 13)
        self.assertEqual(sorted.index_search('oscar'), 14)
        self.assertEqual(sorted.index_search('papa'), 15)
        self.assertEqual(sorted.index_search('quebec'), 16)
        self.assertEqual(sorted.index_search('romeo'), 17)
        self.assertEqual(sorted.index_search('sierra'), 18)
        self.assertEqual(sorted.index_search('tango'), 19)
        self.assertEqual(sorted.index_search('uniform'), 20)
        self.assertEqual(sorted.index_search('victor'), 21)
        self.assertEqual(sorted.index_search('whiskey'), 22)
        self.assertEqual(sorted.index_search('x-ray'), 23)
        self.assertEqual(sorted.index_search('yankee'), 24)
        self.assertEqual(sorted.index_search('zulu'), 25)
        self.assertRaises(NotFoundError, sorted.index_search, 'john')
        self.assertRaises(NotFoundError, sorted.index_search, 'john', partial=True)
        self.assertEqual(sorted.index_search('able', nearest=True), 0)
        self.assertFalse(sorted.index_search('able', nearest=True))
        self.assertEqual(sorted.index_search('alp', partial=True), 0)
        self.assertTrue(sorted.index_search('alp', partial=True))
        self.assertEqual(sorted.index_search('john', nearest=True), 9)
        self.assertFalse(sorted.index_search('john', nearest=True))
        self.assertEqual(sorted.index_search('jul', partial=True), 9)
        self.assertTrue(sorted.index_search('jul', partial=True))

    def test_mismatched_extensions(self):
        old_memo_name = self.dbf_table._meta.memoname
        new_memo_name = old_memo_name[:-3] + 'Dbt'
        os.rename(old_memo_name, new_memo_name)
        table = Table(self.dbf_table._meta.filename)
        self.assertEqual(table._meta.memoname, new_memo_name)
        with table:
            for rec, desc in zip(table, self.dbf_desclist):
                self.assertEqual(rec.desc, desc)
        #
        old_memo_name = self.vfp_table._meta.memoname
        new_memo_name = old_memo_name[:-3] + 'fPt'
        os.rename(old_memo_name, new_memo_name)
        table = Table(self.vfp_table._meta.filename)
        self.assertEqual(table._meta.memoname, new_memo_name)
        with table:
            for rec, desc in zip(table, self.vfp_desclist):
                self.assertEqual(rec.desc, desc)
